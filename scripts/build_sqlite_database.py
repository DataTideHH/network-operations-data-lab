"""Build the local SQLite representation of the public-safe sample data."""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.workflow import DEFAULT_DATABASE, REPO_ROOT, build_database


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the network-operations SQLite sample database."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help="Output database path (default: data/processed/network_operations.db).",
    )
    parser.add_argument(
        "--no-replace",
        action="store_true",
        help="Fail instead of replacing an existing output database.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        counts = build_database(
            args.database,
            replace=not args.no_replace,
        )
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    except Exception as exc:
        print(f"ERROR: SQLite build failed: {exc}")
        return 1

    try:
        display_path = args.database.resolve().relative_to(REPO_ROOT)
    except ValueError:
        display_path = args.database.resolve()

    print("SQLite database built successfully.")
    print(f"Devices: {counts['devices']}")
    print(f"Interfaces: {counts['interfaces']}")
    print(f"Topology links: {counts['topology_links']}")
    print(f"Database: {display_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
