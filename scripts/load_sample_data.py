"""Load and summarize the three public-safe CSV sample tables."""

from __future__ import annotations

from collections import Counter

from scripts.workflow import load_sample_rows


def main() -> int:
    try:
        devices, interfaces, links = load_sample_rows()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print("Network operations sample-data summary")
    print("=" * 38)
    print(f"Devices:       {len(devices)}")
    print(f"Interfaces:    {len(interfaces)}")
    print(f"Topology links:{len(links):>5}")

    print("\nInterface operational status")
    for status, count in sorted(
        Counter(row["oper_status"].strip().lower() for row in interfaces).items()
    ):
        print(f"- {status}: {count}")

    print("\nPort roles")
    for role, count in sorted(
        Counter(row["port_role"].strip().lower() for row in interfaces).items()
    ):
        print(f"- {role}: {count}")

    print("\nTopology link status")
    for status, count in sorted(
        Counter(row["link_status"].strip().lower() for row in links).items()
    ):
        print(f"- {status}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
