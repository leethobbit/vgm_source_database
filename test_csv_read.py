"""Test CSV reading."""
import csv
from pathlib import Path

csv_dir = Path("dev_reference")
csv_files = list(csv_dir.glob("NEWER VGM Sound Sources - *.csv"))

print(f"Found {len(csv_files)} CSV files")

if csv_files:
    test_file = csv_files[0]
    print(f"\nTesting: {test_file.name}")
    
    with open(test_file, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        print(f"Headers: {headers}")
        
        count = 0
        for row_idx, row in enumerate(reader, start=2):
            if count < 20:  # First 20 rows
                company = row.get("Company/Manufacturer", "").strip()
                product = row.get("Product", "").strip()
                print(f"Row {row_idx}: Company='{company[:50]}', Product='{product[:30]}'")
                count += 1
            else:
                break
