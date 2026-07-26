from __future__ import annotations

from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from scripts.workflow import (
    DEFAULT_REPORT,
    REPO_ROOT,
    SAMPLE_DIR,
    build_database,
    fetch_analysis_views,
    fetch_quality_results,
    load_sample_rows,
    parse_bool,
    parse_non_negative_int,
    write_quality_report,
)


class NetworkOperationsWorkflowTest(unittest.TestCase):
    def test_sample_headers_and_row_counts(self) -> None:
        devices, interfaces, links = load_sample_rows()
        self.assertEqual(5, len(devices))
        self.assertEqual(5, len(interfaces))
        self.assertEqual(3, len(links))

    def test_boolean_parser_rejects_uncontrolled_values(self) -> None:
        self.assertEqual(1, parse_bool("true", "field"))
        self.assertEqual(0, parse_bool("FALSE", "field"))
        with self.assertRaisesRegex(ValueError, "must be 'true' or 'false'"):
            parse_bool("yes", "field")

    def test_integer_parser_rejects_negative_and_non_decimal_values(self) -> None:
        self.assertEqual(1000, parse_non_negative_int("1000", "speed"))
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            parse_non_negative_int("-1", "speed")
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            parse_non_negative_int("1.5", "speed")

    def test_sqlite_build_enforces_relationships_and_counts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "lab.db"
            counts = build_database(database)
            self.assertEqual(
                {"devices": 5, "interfaces": 5, "topology_links": 3},
                counts,
            )
            connection = sqlite3.connect(database)
            try:
                self.assertEqual(
                    [],
                    connection.execute("PRAGMA foreign_key_check").fetchall(),
                )
                self.assertEqual(
                    5,
                    connection.execute("SELECT COUNT(*) FROM devices").fetchone()[0],
                )
                self.assertEqual(
                    5,
                    connection.execute("SELECT COUNT(*) FROM interfaces").fetchone()[0],
                )
                self.assertEqual(
                    3,
                    connection.execute(
                        "SELECT COUNT(*) FROM topology_links"
                    ).fetchone()[0],
                )
            finally:
                connection.close()

    def test_analysis_views_are_installed_and_queryable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "lab.db"
            build_database(database)
            views = fetch_analysis_views(database)
        self.assertEqual(
            {
                "device_count_by_role",
                "interface_status_summary",
                "port_role_summary",
                "topology_link_status_summary",
                "documentation_coverage",
            },
            set(views),
        )
        self.assertEqual(
            100.0,
            views["documentation_coverage"][0]["description_coverage_pct"],
        )

    def test_quality_report_separates_data_failures_from_operational_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "lab.db"
            build_database(database)
            results = fetch_quality_results(database)

        failures = [
            row
            for row in results
            if row["category"] == "data_quality" and row["status"] == "FAIL"
        ]
        warnings = [
            row
            for row in results
            if row["category"] == "operational_condition"
            and row["status"] == "WARN"
        ]
        self.assertEqual([], failures)
        self.assertEqual(1, len(warnings))
        self.assertEqual(11, warnings[0]["check_no"])
        self.assertEqual(1, warnings[0]["affected_rows"])

    def test_committed_report_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "lab.db"
            generated = Path(directory) / "report.csv"
            build_database(database)
            write_quality_report(fetch_quality_results(database), generated)
            self.assertEqual(
                DEFAULT_REPORT.read_bytes(),
                generated.read_bytes(),
            )

    def test_invalid_boolean_fails_before_database_is_published(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sample_dir = Path(directory) / "sample"
            shutil.copytree(SAMPLE_DIR, sample_dir)
            devices = sample_dir / "devices.csv"
            devices.write_text(
                devices.read_text(encoding="utf-8").replace(
                    "endpoint,true",
                    "endpoint,yes",
                    1,
                ),
                encoding="utf-8",
            )
            database = Path(directory) / "invalid.db"
            with self.assertRaisesRegex(ValueError, "must be 'true' or 'false'"):
                build_database(database, sample_dir=sample_dir)
            self.assertFalse(database.exists())

    def test_unknown_topology_target_fails_foreign_key_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sample_dir = Path(directory) / "sample"
            shutil.copytree(SAMPLE_DIR, sample_dir)
            links = sample_dir / "topology_links.csv"
            links.write_text(
                links.read_text(encoding="utf-8").replace(
                    "dev-004,unknown",
                    "dev-999,unknown",
                    1,
                ),
                encoding="utf-8",
            )
            database = Path(directory) / "invalid.db"
            with self.assertRaises(sqlite3.IntegrityError):
                build_database(database, sample_dir=sample_dir)
            self.assertFalse(database.exists())

    def test_device_name_mismatch_is_reported_as_data_quality_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "lab.db"
            build_database(database)
            connection = sqlite3.connect(database)
            try:
                connection.execute(
                    """
                    UPDATE interfaces
                    SET device_name = 'LAB_ROUTER'
                    WHERE interface_id = 'int-001'
                    """
                )
                connection.commit()
            finally:
                connection.close()
            results = fetch_quality_results(database)

        mismatch = next(row for row in results if row["check_no"] == 36)
        self.assertEqual("FAIL", mismatch["status"])
        self.assertEqual(1, mismatch["affected_rows"])

    def test_cli_workflow_runs_without_external_dependencies(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "scripts.run_sqlite_analysis"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("documentation_coverage", completed.stdout)


if __name__ == "__main__":
    unittest.main()
