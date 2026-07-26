"""Build a temporary SQLite database and print the analysis views."""

from __future__ import annotations

import tempfile
from pathlib import Path

from scripts.workflow import build_database, fetch_analysis_views


def main() -> int:
    try:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "network_operations.db"
            build_database(database_path)
            views = fetch_analysis_views(database_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    except Exception as exc:
        print(f"ERROR: SQLite analysis failed: {exc}")
        return 1

    print("SQLite analysis views")
    print("=" * 21)
    for view_name, rows in views.items():
        print(f"\n{view_name}")
        for row in rows:
            rendered = ", ".join(f"{key}={value}" for key, value in row.items())
            print(f"- {rendered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
