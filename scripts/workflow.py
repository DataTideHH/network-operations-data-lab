"""Core CSV, SQLite and reporting workflow for the public-safe sample data."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Iterable, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = REPO_ROOT / "data" / "sample"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
SCHEMA_SQL = REPO_ROOT / "sql" / "schema.sql"
ANALYSIS_SQL = REPO_ROOT / "sql" / "sample_analysis.sql"
QUALITY_SQL = REPO_ROOT / "sql" / "data_quality_checks.sql"
DEFAULT_DATABASE = PROCESSED_DIR / "network_operations.db"
DEFAULT_REPORT = PROCESSED_DIR / "data_quality_report.csv"

DEVICE_COLUMNS = [
    "device_id",
    "device_name",
    "device_type",
    "vendor",
    "model",
    "role",
    "location",
    "location_scope",
    "management_scope",
    "is_active",
]

INTERFACE_COLUMNS = [
    "device_id",
    "device_name",
    "interface_id",
    "interface_name",
    "interface_type",
    "admin_status",
    "oper_status",
    "vlan",
    "port_role",
    "speed_mbps",
    "duplex",
    "description",
    "description_present",
    "expected_downstream_devices",
]

TOPOLOGY_COLUMNS = [
    "link_id",
    "source_device_id",
    "source_interface_id",
    "target_device_id",
    "target_interface_id",
    "link_role",
    "link_status",
    "expected_downstream_devices",
]

REPORT_COLUMNS = [
    "check_no",
    "check_name",
    "category",
    "status",
    "affected_rows",
    "description",
]

ANALYSIS_VIEWS = [
    "device_count_by_role",
    "interface_status_summary",
    "port_role_summary",
    "topology_link_status_summary",
    "documentation_coverage",
]


def read_csv_rows(path: Path, expected_columns: Sequence[str]) -> list[dict[str, str]]:
    """Read one CSV file and enforce its complete ordered header contract."""
    if not path.exists():
        raise FileNotFoundError(f"Expected sample file not found: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        if header != list(expected_columns):
            raise ValueError(
                f"{path.name} header mismatch.\n"
                f"Expected: {list(expected_columns)}\n"
                f"Actual:   {header}"
            )
        rows = list(reader)

    if not rows:
        raise ValueError(f"{path.name} must contain at least one data row.")
    return rows


def parse_bool(value: str, field_name: str) -> int:
    normalized = value.strip().lower()
    if normalized == "true":
        return 1
    if normalized == "false":
        return 0
    raise ValueError(f"{field_name} must be 'true' or 'false', got {value!r}")


def parse_non_negative_int(value: str, field_name: str) -> int:
    normalized = value.strip()
    if not normalized or not normalized.isascii() or not normalized.isdigit():
        raise ValueError(f"{field_name} must be a non-negative integer, got {value!r}")
    return int(normalized)


def load_sample_rows(
    sample_dir: Path = SAMPLE_DIR,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    devices = read_csv_rows(sample_dir / "devices.csv", DEVICE_COLUMNS)
    interfaces = read_csv_rows(sample_dir / "interfaces.csv", INTERFACE_COLUMNS)
    topology_links = read_csv_rows(
        sample_dir / "topology_links.csv",
        TOPOLOGY_COLUMNS,
    )
    return devices, interfaces, topology_links


def _device_values(row: dict[str, str]) -> tuple[object, ...]:
    return (
        row["device_id"].strip(),
        row["device_name"].strip(),
        row["device_type"].strip().lower(),
        row["vendor"].strip(),
        row["model"].strip(),
        row["role"].strip().lower(),
        row["location"].strip(),
        row["location_scope"].strip().lower(),
        row["management_scope"].strip().lower(),
        parse_bool(row["is_active"], "devices.is_active"),
    )


def _interface_values(row: dict[str, str]) -> tuple[object, ...]:
    return (
        row["interface_id"].strip(),
        row["device_id"].strip(),
        row["device_name"].strip(),
        row["interface_name"].strip(),
        row["interface_type"].strip(),
        row["admin_status"].strip().lower(),
        row["oper_status"].strip().lower(),
        row["vlan"].strip(),
        row["port_role"].strip().lower(),
        parse_non_negative_int(row["speed_mbps"], "interfaces.speed_mbps"),
        row["duplex"].strip().lower(),
        row["description"].strip(),
        parse_bool(
            row["description_present"],
            "interfaces.description_present",
        ),
        row["expected_downstream_devices"].strip().lower(),
    )


def _topology_values(row: dict[str, str]) -> tuple[object, ...]:
    return (
        row["link_id"].strip(),
        row["source_device_id"].strip(),
        row["source_interface_id"].strip(),
        row["target_device_id"].strip(),
        row["target_interface_id"].strip(),
        row["link_role"].strip().lower(),
        row["link_status"].strip().lower(),
        row["expected_downstream_devices"].strip().lower(),
    )


def install_sql_views(connection: sqlite3.Connection) -> None:
    connection.executescript(ANALYSIS_SQL.read_text(encoding="utf-8"))
    connection.executescript(QUALITY_SQL.read_text(encoding="utf-8"))


def build_database(
    database_path: Path = DEFAULT_DATABASE,
    *,
    sample_dir: Path = SAMPLE_DIR,
    replace: bool = True,
) -> dict[str, int]:
    """Create a reproducible SQLite database from the three sample CSV files."""
    devices, interfaces, topology_links = load_sample_rows(sample_dir)

    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    if database_path.exists():
        if not replace:
            raise FileExistsError(f"Database already exists: {database_path}")
        database_path.unlink()

    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))

        with connection:
            connection.executemany(
                """
                INSERT INTO devices (
                    device_id, device_name, device_type, vendor, model, role,
                    location, location_scope, management_scope, is_active
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [_device_values(row) for row in devices],
            )
            connection.executemany(
                """
                INSERT INTO interfaces (
                    interface_id, device_id, device_name, interface_name,
                    interface_type, admin_status, oper_status, vlan, port_role,
                    speed_mbps, duplex, description, description_present,
                    expected_downstream_devices
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [_interface_values(row) for row in interfaces],
            )
            connection.executemany(
                """
                INSERT INTO topology_links (
                    link_id, source_device_id, source_interface_id,
                    target_device_id, target_interface_id, link_role,
                    link_status, expected_downstream_devices
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [_topology_values(row) for row in topology_links],
            )
            install_sql_views(connection)

        foreign_key_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()
        if foreign_key_errors:
            raise ValueError(
                f"SQLite foreign-key validation failed: {foreign_key_errors}"
            )

        return {
            "devices": len(devices),
            "interfaces": len(interfaces),
            "topology_links": len(topology_links),
        }
    except Exception:
        connection.close()
        if database_path.exists():
            database_path.unlink()
        raise
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            pass


def fetch_quality_results(
    database_path: Path,
) -> list[dict[str, object]]:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT
                check_no,
                check_name,
                category,
                status,
                affected_rows,
                description
            FROM data_quality_results
            ORDER BY check_no, check_name
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def write_quality_report(
    results: Iterable[dict[str, object]],
    report_path: Path = DEFAULT_REPORT,
) -> None:
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_COLUMNS)
        writer.writeheader()
        writer.writerows(results)


def fetch_analysis_views(
    database_path: Path,
) -> dict[str, list[dict[str, object]]]:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        return {
            view: [
                dict(row)
                for row in connection.execute(f"SELECT * FROM {view}").fetchall()
            ]
            for view in ANALYSIS_VIEWS
        }
    finally:
        connection.close()
