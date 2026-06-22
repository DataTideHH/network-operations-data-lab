from csv import DictReader
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "sample"


def load_csv(filename: str) -> list[dict[str, str]]:
    path = DATA_DIR / filename

    with path.open(newline="", encoding="utf-8") as file:
        return list(DictReader(file))


devices = load_csv("devices.csv")
interfaces = load_csv("interfaces.csv")

print("Devices")
for device in devices:
    print(device)

print("\nInterfaces")
for interface in interfaces:
    print(interface)

status_summary = Counter(
    (row["admin_status"], row["oper_status"])
    for row in interfaces
)

print("\nInterface status summary")
for (admin_status, oper_status), count in status_summary.items():
    print(f"{admin_status=}, {oper_status=}, count={count}")

port_role_summary = Counter(
    row["port_role"]
    for row in interfaces
)

print("\nPort role summary")
for port_role, count in port_role_summary.items():
    print(f"{port_role=}, count={count}")
