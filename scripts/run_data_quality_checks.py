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

It reads the two sample CSV files, runs every check, prints a short console
summary and writes a public-safe report to
``data/processed/data_quality_report.csv``.

Public-safe: the report contains only the check number, name, category, status,
affected count and a short description. It never writes device names, interface
names or any other row-level identifier, so the output is safe for a public
repository.

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
REPORT_CSV = PROCESSED_DIR / "data_quality_report.csv"

EXPECTED_DEVICE_COLUMNS = [
    "device_id", "device_name", "device_type", "vendor", "model", "role", "location",
]
EXPECTED_INTERFACE_COLUMNS = [
    "device_name", "interface_name", "interface_type",
    "admin_status", "oper_status", "vlan", "port_role", "description",
]


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
# Checks 1-17 (numbered to match sql/data_quality_checks.sql)
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

    # 15. Device count by role  (SQL #15) -- public-safe: distinct role count only
    role_counts = Counter(norm(d["role"]) for d in devices)
    record(15, "Device count by role (distinct roles)", "summary", len(role_counts),
           "Number of distinct device roles present in devices.csv.")

    # 16. Interface status summary  (SQL #16) -- distinct admin/oper combinations
    status_combos = {(norm(i["admin_status"]), norm(i["oper_status"])) for i in interfaces}
    record(16, "Interface status summary (distinct combinations)", "summary", len(status_combos),
           "Number of distinct admin_status/oper_status combinations.")

    # 17. Port role summary  (SQL #17) -- distinct port-role count
    port_roles = {norm(i["port_role"]) for i in interfaces}
    record(17, "Port role summary (distinct roles)", "summary", len(port_roles),
           "Number of distinct port roles present in interfaces.csv.")


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
    run_checks(devices, interfaces)
    write_report()
    print_summary()


if __name__ == "__main__":
    main()
