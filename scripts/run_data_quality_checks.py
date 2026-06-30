"""Run public-safe data-quality checks on the network operations sample data.

This script mirrors the numbered data-quality check logic from
``sql/data_quality_checks.sql``, but writes a compact, public-safe report rather
than reproducing the SQL result sets verbatim. Each check below carries the same
number as in the SQL file, so the two stay conceptually in sync.

Note on the duplicate checks (3, 5, 8): the SQL versions use
``GROUP BY ... HAVING COUNT(*) > 1`` and therefore return the duplicate *groups*.
This report instead counts the *affected rows* (how many records are involved),
which is the more practical figure for a data-quality summary. Blank values are
deliberately excluded from the duplicate checks, because missing values are
already covered by their own checks (2, 4, 6, 7) -- so "missing" and "duplicate"
stay cleanly separated.

It is intentionally dependency-free: it uses only the Python standard library
(``csv``, ``pathlib``, ``collections``), matching the lightweight style of
``scripts/load_sample_data.py``. No pandas, no external packages, no
``requirements.txt`` needed.

It reads the three sample CSV files, runs every check, prints a short console
summary and writes a public-safe report to
``data/processed/data_quality_report.csv``.

Public-safe: the report contains only the check number, name, category, status,
affected count and a short description. It never writes device names, interface
names, link IDs or any other row-level identifier, so the output is safe for a
public repository.

--------------------------------------------------------------------------
Checks 18-31 (added on top of the original 1-17, devices/interfaces only):
--------------------------------------------------------------------------
These extend the report to data/sample/topology_links.csv and to the richer
interfaces.csv schema (device_id, interface_id, description_present,
expected_downstream_devices). The original checks 1-17 are unchanged.

Note: topology_links.target_interface_id is intentionally NOT validated against
interfaces.csv. Client endpoints (LAB_CLIENT_A, LAB_CLIENT_B, ...) do not have
their own interface rows in interfaces.csv, so target_interface_id is "unknown"
by design for client-facing links. Only target_device_id is checked (29).

Run from anywhere inside the repository:

    python scripts/run_data_quality_checks.py
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

def find_repo_root(marker_parts: tuple[str, ...] = ("data", "sample")) -> Path:
    """Walk up from this file until data/sample is found.

    Anchoring on the script location (not the current working directory) makes
    the script robust regardless of where it is invoked from.
    """
    start = Path(__file__).resolve().parent
    for candidate in [start, *start.parents]:
        if (candidate.joinpath(*marker_parts)).exists():
            return candidate
    raise FileNotFoundError(
        f"Could not locate the repository root (no data/sample found above {start})."
    )


REPO_ROOT = find_repo_root()
SAMPLE_DIR = REPO_ROOT / "data" / "sample"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
DEVICES_CSV = SAMPLE_DIR / "devices.csv"
INTERFACES_CSV = SAMPLE_DIR / "interfaces.csv"
TOPOLOGY_CSV = SAMPLE_DIR / "topology_links.csv"
REPORT_CSV = PROCESSED_DIR / "data_quality_report.csv"

EXPECTED_DEVICE_COLUMNS = [
    "device_id", "device_name", "device_type", "vendor", "model", "role", "location",
]
# Extended to cover the columns the new checks (19-26) rely on. The original
# columns are untouched, so checks 1-17 keep working exactly as before.
EXPECTED_INTERFACE_COLUMNS = [
    "device_id", "device_name", "interface_id", "interface_name", "interface_type",
    "admin_status", "oper_status", "vlan", "port_role", "description",
    "description_present", "expected_downstream_devices",
]
EXPECTED_TOPOLOGY_COLUMNS = [
    "link_id", "source_device_id", "source_interface_id",
    "target_device_id", "target_interface_id",
    "link_role", "link_status", "expected_downstream_devices",
]

# Adjust this list if new port roles are introduced in interfaces.csv.
ALLOWED_PORT_ROLES = {
    "access", "trunk", "uplink", "client_access", "lab_access", "bridge_uplink",
}


# --------------------------------------------------------------------------
# Small helpers that mirror the SQL semantics
# --------------------------------------------------------------------------

def is_blank(value: str | None) -> bool:
    """True if value is missing or whitespace-only.

    Mirrors the SQL pattern ``col IS NULL OR TRIM(col) = ''``.
    """
    return value is None or value.strip() == ""


def norm(value: str | None) -> str:
    """Lower-cased, trimmed value (mirrors ``LOWER(TRIM(col))``)."""
    return "" if value is None else value.strip().lower()


# --------------------------------------------------------------------------
# Result collection
# --------------------------------------------------------------------------

results: list[dict] = []


def record(number: int, name: str, category: str, affected: int, description: str) -> None:
    """Store one check result.

    category:
      - "issue"   : affected > 0 is a data-quality problem (status OK / FAIL)
      - "summary" : descriptive count, never a failure (status INFO)
    """
    if category == "summary":
        status = "INFO"
    else:
        status = "OK" if affected == 0 else "FAIL"
    results.append(
        {
            "check_no": number,
            "check_name": name,
            "category": category,
            "status": status,
            "affected_rows": int(affected),
            "description": description,
        }
    )


# --------------------------------------------------------------------------
# Load data
# --------------------------------------------------------------------------

def read_csv_dicts(path: Path, expected_columns: list[str]) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Expected sample file not found: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        missing = [col for col in expected_columns if col not in header]
        if missing:
            raise ValueError(f"{path.name} is missing columns: {missing}")
        return list(reader)


# --------------------------------------------------------------------------
# Checks 1-17 (numbered to match sql/data_quality_checks.sql) -- unchanged
# --------------------------------------------------------------------------

def run_checks(devices: list[dict], interfaces: list[dict]) -> None:
    # 1. Row counts  (SQL #1)
    record(1, "Row count: devices", "summary", len(devices),
           "Total number of rows in devices.csv.")
    record(1, "Row count: interfaces", "summary", len(interfaces),
           "Total number of rows in interfaces.csv.")

    # 2. Missing device identifiers  (SQL #2)
    n = sum(1 for d in devices if is_blank(d["device_id"]))
    record(2, "Missing device identifiers", "issue", n,
           "Devices with a missing or empty device_id.")

    # 3. Duplicate device IDs  (SQL #3)
    id_counts = Counter(d["device_id"].strip() for d in devices if not is_blank(d["device_id"]))
    n = sum(count for count in id_counts.values() if count > 1)
    record(3, "Duplicate device IDs", "issue", n,
           "Rows sharing a non-empty device_id with at least one other row.")

    # 4. Missing device names  (SQL #4)
    n = sum(1 for d in devices if is_blank(d["device_name"]))
    record(4, "Missing device names", "issue", n,
           "Devices with a missing or empty device_name.")

    # 5. Duplicate device names  (SQL #5)
    name_counts = Counter(d["device_name"].strip() for d in devices if not is_blank(d["device_name"]))
    n = sum(count for count in name_counts.values() if count > 1)
    record(5, "Duplicate device names", "issue", n,
           "Rows sharing a non-empty device_name with at least one other row.")

    # 6. Missing interface device references  (SQL #6)
    n = sum(1 for i in interfaces if is_blank(i["device_name"]))
    record(6, "Missing interface device references", "issue", n,
           "Interfaces with a missing or empty device_name reference.")

    # 7. Missing interface names  (SQL #7)
    n = sum(1 for i in interfaces if is_blank(i["interface_name"]))
    record(7, "Missing interface names", "issue", n,
           "Interfaces with a missing or empty interface_name.")

    # 8. Duplicate interface rows per device  (SQL #8)
    pair_counts = Counter(
        (i["device_name"], i["interface_name"]) for i in interfaces
    )
    n = sum(count for count in pair_counts.values() if count > 1)
    record(8, "Duplicate interface rows per device", "issue", n,
           "Rows sharing the same device_name + interface_name with another row.")

    # 9. Interfaces referencing unknown devices  (SQL #9, LEFT JOIN ... IS NULL)
    known_devices = {d["device_name"] for d in devices if not is_blank(d["device_name"])}
    n = sum(1 for i in interfaces if i["device_name"] not in known_devices)
    record(9, "Interfaces referencing unknown devices", "issue", n,
           "Interfaces whose device_name does not exist in devices.csv.")

    # 10. Missing administrative or operational status  (SQL #10)
    n = sum(1 for i in interfaces if is_blank(i["admin_status"]) or is_blank(i["oper_status"]))
    record(10, "Missing administrative or operational status", "issue", n,
           "Interfaces with a missing admin_status or oper_status.")

    # 11. Interfaces administratively up but operationally down  (SQL #11)
    down_values = {"down", "notconnect", "not connected"}
    n = sum(
        1 for i in interfaces
        if norm(i["admin_status"]) == "up" and norm(i["oper_status"]) in down_values
    )
    record(11, "Admin up but operationally down", "issue", n,
           "Interfaces admin up while operationally down/notconnect.")

    # 12. Access ports without VLAN documentation  (SQL #12)
    n = sum(
        1 for i in interfaces
        if norm(i["port_role"]) == "access" and is_blank(i["vlan"])
    )
    record(12, "Access ports without VLAN documentation", "issue", n,
           "Access ports with a missing or empty vlan value.")

    # 13. Trunk ports without trunk documentation in the VLAN field  (SQL #13)
    n = sum(
        1 for i in interfaces
        if norm(i["port_role"]) == "trunk" and norm(i["vlan"]) != "trunk"
    )
    record(13, "Trunk ports without trunk documentation", "issue", n,
           "Trunk ports whose vlan field is not set to 'trunk'.")

    # 14. Missing interface descriptions  (SQL #14)
    n = sum(1 for i in interfaces if is_blank(i["description"]))
    record(14, "Missing interface descriptions", "issue", n,
           "Interfaces with a missing or empty description.")

    # 15. Device count by role (SQL #15) -- public-safe: distinct role count only
    role_counts = Counter(norm(d["role"]) for d in devices)
    record(15, "Device count by role (distinct roles)", "summary", len(role_counts),
           "Number of distinct device roles present in devices.csv.")

    # 16. Interface status summary (SQL #16) -- distinct admin/oper combinations
    status_combos = {(norm(i["admin_status"]), norm(i["oper_status"])) for i in interfaces}
    record(16, "Interface status summary (distinct combinations)", "summary", len(status_combos),
           "Number of distinct admin_status/oper_status combinations.")

    # 17. Port role summary (SQL #17) -- distinct port-role count
    port_roles = {norm(i["port_role"]) for i in interfaces}
    record(17, "Port role summary (distinct roles)", "summary", len(port_roles),
           "Number of distinct port roles present in interfaces.csv.")


# --------------------------------------------------------------------------
# Checks 18-31 -- topology_links.csv + extended interfaces.csv schema
# --------------------------------------------------------------------------

def run_topology_checks(devices: list[dict], interfaces: list[dict], links: list[dict]) -> None:
    # 18. Row count: topology_links (file presence + expected columns are
    #     already enforced by read_csv_dicts before this function runs, same
    #     hard-fail pattern as devices.csv/interfaces.csv above; this entry
    #     just confirms successful load with a row count, same as check 1).
    record(18, "Row count: topology_links", "summary", len(links),
           "Total number of rows in topology_links.csv.")

    known_device_ids = {d["device_id"].strip() for d in devices if not is_blank(d["device_id"])}

    # 19. interfaces.device_id must exist in devices.csv
    n = sum(1 for i in interfaces if i["device_id"].strip() not in known_device_ids)
    record(19, "Interfaces with unknown device_id", "issue", n,
           "Interfaces whose device_id does not exist in devices.csv.")

    # 20. Duplicate interface_id in interfaces.csv
    iface_id_counts = Counter(
        i["interface_id"].strip() for i in interfaces if not is_blank(i["interface_id"])
    )
    n = sum(count for count in iface_id_counts.values() if count > 1)
    record(20, "Duplicate interface IDs", "issue", n,
           "Rows in interfaces.csv sharing a non-empty interface_id with another row.")

    # 21. Duplicate device_id + interface_name in interfaces.csv
    pair_counts = Counter(
        (i["device_id"].strip(), i["interface_name"].strip()) for i in interfaces
    )
    n = sum(count for count in pair_counts.values() if count > 1)
    record(21, "Duplicate device_id + interface_name pairs", "issue", n,
           "Rows sharing the same device_id + interface_name with another row.")

    # 22. port_role not in allowed value list
    n = sum(1 for i in interfaces if norm(i["port_role"]) not in ALLOWED_PORT_ROLES)
    record(22, "Interfaces with unexpected port_role", "issue", n,
           f"port_role outside the allowed list: {sorted(ALLOWED_PORT_ROLES)}.")

    # 23. description_present must be true/false
    allowed_bool = {"true", "false"}
    n = sum(1 for i in interfaces if norm(i["description_present"]) not in allowed_bool)
    record(23, "Invalid description_present values", "issue", n,
           "description_present values other than 'true' or 'false'.")

    # 24. Active interfaces (admin=up AND oper=up) without a description
    n = sum(
        1 for i in interfaces
        if norm(i["admin_status"]) == "up" and norm(i["oper_status"]) == "up"
        and is_blank(i["description"])
    )
    record(24, "Active interfaces without description", "issue", n,
           "Interfaces with admin_status=up and oper_status=up but an empty description.")

    # 25. uplink interfaces should have expected_downstream_devices=multiple
    n = sum(
        1 for i in interfaces
        if norm(i["port_role"]) == "uplink"
        and norm(i["expected_downstream_devices"]) != "multiple"
    )
    record(25, "Uplink interfaces with unexpected downstream cardinality", "issue", n,
           "port_role=uplink interfaces where expected_downstream_devices is not 'multiple'.")

    # 26. client_access interfaces should have expected_downstream_devices=single
    n = sum(
        1 for i in interfaces
        if norm(i["port_role"]) == "client_access"
        and norm(i["expected_downstream_devices"]) != "single"
    )
    record(26, "client_access interfaces with unexpected downstream cardinality", "issue", n,
           "port_role=client_access interfaces where expected_downstream_devices is not 'single'.")

    # 27. topology_links.source_device_id must exist in devices.csv
    n = sum(1 for l in links if l["source_device_id"].strip() not in known_device_ids)
    record(27, "Topology links with unknown source_device_id", "issue", n,
           "Links whose source_device_id does not exist in devices.csv.")

    # 28. topology_links.source_interface_id must exist for that device in interfaces.csv
    known_iface_pairs = {
        (i["device_id"].strip(), i["interface_id"].strip()) for i in interfaces
    }
    n = sum(
        1 for l in links
        if (l["source_device_id"].strip(), l["source_interface_id"].strip()) not in known_iface_pairs
    )
    record(28, "Topology links with unknown source_interface_id", "issue", n,
           "Links whose (source_device_id, source_interface_id) pair does not exist in interfaces.csv.")

    # 29. topology_links.target_device_id must exist in devices.csv
    # Note: target_interface_id is deliberately not validated -- client
    # endpoints have no interface row and use "unknown" by design.
    n = sum(1 for l in links if l["target_device_id"].strip() not in known_device_ids)
    record(29, "Topology links with unknown target_device_id", "issue", n,
           "Links whose target_device_id does not exist in devices.csv.")

    # 30. active link must have a source interface with oper_status=up
    iface_oper_status = {
        (i["device_id"].strip(), i["interface_id"].strip()): norm(i["oper_status"])
        for i in interfaces
    }
    n = sum(
        1 for l in links
        if norm(l["link_status"]) == "active"
        and iface_oper_status.get(
            (l["source_device_id"].strip(), l["source_interface_id"].strip())
        ) != "up"
    )
    record(30, "Active links with source interface not operationally up", "issue", n,
           "link_status=active links whose source interface is missing or not oper_status=up.")

    # 31. link_role should match the port_role of the source interface
    iface_port_role = {
        (i["device_id"].strip(), i["interface_id"].strip()): norm(i["port_role"])
        for i in interfaces
    }
    n = sum(
        1 for l in links
        if iface_port_role.get(
            (l["source_device_id"].strip(), l["source_interface_id"].strip())
        ) not in (None, norm(l["link_role"]))
    )
    record(31, "Links where link_role does not match source port_role", "issue", n,
           "Links whose link_role differs from the port_role of their source interface "
           "(links with an unresolved source interface are excluded here -- see check 28).")


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

REPORT_FIELDS = ["check_no", "check_name", "category", "status", "affected_rows", "description"]


def write_report() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(results)


def print_summary() -> None:
    issues = [r for r in results if r["category"] == "issue"]
    failed = [r for r in issues if r["status"] == "FAIL"]
    passed = [r for r in issues if r["status"] == "OK"]

    print("Network operations data-quality report")
    print("=" * 39)
    for r in results:
        print(f"[{r['check_no']:>2}] {r['status']:<4} {r['check_name']} "
              f"(affected: {r['affected_rows']})")
    print()
    print(f"Issue checks run:    {len(issues)}")
    print(f"Issue checks passed: {len(passed)}")
    print(f"Issue checks failed: {len(failed)}")
    if failed:
        print()
        print("Checks needing attention:")
        for r in failed:
            print(f"  - [{r['check_no']:>2}] {r['check_name']}: {r['affected_rows']} affected row(s)")
    print()
    print(f"Report written to: {REPORT_CSV.relative_to(REPO_ROOT)}")


def main() -> None:
    devices = read_csv_dicts(DEVICES_CSV, EXPECTED_DEVICE_COLUMNS)
    interfaces = read_csv_dicts(INTERFACES_CSV, EXPECTED_INTERFACE_COLUMNS)
    links = read_csv_dicts(TOPOLOGY_CSV, EXPECTED_TOPOLOGY_COLUMNS)
    run_checks(devices, interfaces)
    run_topology_checks(devices, interfaces, links)
    write_report()
    print_summary()


if __name__ == "__main__":
    main()
