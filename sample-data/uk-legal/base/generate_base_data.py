"""
Validate the UK legal base dataset.

Run this script to verify files exist and print row counts.
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FILES = [
    "customers.csv",
    "cases.csv",
    "solicitors.csv",
    "transactions.csv",
    "interactions.csv",
]


def count_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        _ = next(reader, None)
        return sum(1 for _ in reader)


def main() -> int:
    print("Validating UK legal base dataset...\n")

    missing = []
    total = 0
    for name in FILES:
        file_path = BASE_DIR / name
        if not file_path.exists():
            missing.append(name)
            continue

        rows = count_rows(file_path)
        total += rows
        print(f"- {name}: {rows} rows")

    if missing:
        print("\nMissing files:")
        for name in missing:
            print(f"  - {name}")
        return 1

    print(f"\nTotal rows across base dataset: {total}")
    print("Base dataset is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
