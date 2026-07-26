"""Generate the aggregated public-safe data-quality report."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from scripts.workflow import (
    DEFAULT_REPORT,
    REPO_ROOT,
    build_database,
    fetch_quality_results,
    write_quality_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the public-safe data-quality report."
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help="Output CSV path.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 2 when data-quality checks have FAIL status.",
    )
    return parser.parse_args()


def print_summary(results: list[dict[str, object]], report_path: Path) -> None:
    data_quality = [
        row for row in results if row["category"] == "data_quality"
    ]
    operational = [
        row for row in results if row["category"] == "operational_condition"
    ]
    failures = [row for row in data_quality if row["status"] == "FAIL"]
    warnings = [row for row in operational if row["status"] == "WARN"]

    print("Network operations data-quality report")
    print("=" * 38)
    print(f"Result rows:          {len(results)}")
    print(f"Data-quality checks:  {len(data_quality)}")
    print(f"Data-quality failures:{len(failures):>3}")
    print(f"Operational warnings:{len(warnings):>3}")

    if warnings:
        print()
        print("Operational conditions requiring review:")
        for row in warnings:
            print(
                f"  - [{int(row['check_no']):>2}] "
                f"{row['check_name']}: {row['affected_rows']} affected row(s)"
            )

    try:
        display_path = report_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        display_path = report_path.resolve()
    print()
    print(f"Report written to: {display_path}")


def main() -> int:
    args = parse_args()
    try:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "network_operations.db"
            build_database(database_path)
            results = fetch_quality_results(database_path)
        write_quality_report(results, args.report)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    except Exception as exc:
        print(f"ERROR: Report generation failed: {exc}")
        return 1

    print_summary(results, args.report)
    has_failures = any(
        row["category"] == "data_quality" and row["status"] == "FAIL"
        for row in results
    )
    return 2 if args.strict and has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
