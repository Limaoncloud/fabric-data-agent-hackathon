"""
Validate Step 1 cleaned baseline dataset.

This repo now starts from cleaned data in step1/*.csv.
Run this script to verify files exist and print row counts.
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FILES = [
    "step1_cleaned_customers.csv",
    "step1_cleaned_cases.csv",
    "step1_cleaned_solicitors.csv",
    "step1_cleaned_transactions.csv",
    "step1_cleaned_interactions.csv",
]


def count_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        _ = next(reader, None)
        return sum(1 for _ in reader)


def main() -> int:
    print("Validating Step 1 cleaned baseline files...\n")

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

    print(f"\nTotal rows across Step 1 cleaned dataset: {total}")
    print("Step 1 baseline dataset is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
