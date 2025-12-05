"""Run CSV conversion with file logging."""
import sys
import traceback
from pathlib import Path

# Redirect output to file
log_file = open("csv_conversion_log.txt", "w", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

try:
    print("Starting CSV conversion...")
    print("=" * 60)
    
    from convert_csv_to_yaml import CSVConverter
    
    csv_dir = "dev_reference"
    output_dir = "fixtures"
    
    print(f"CSV directory: {csv_dir}")
    print(f"Output directory: {output_dir}")
    
    csv_path = Path(csv_dir)
    if not csv_path.exists():
        print(f"ERROR: CSV directory not found: {csv_path}")
        sys.exit(1)
    
    csv_files = list(csv_path.glob("NEWER VGM Sound Sources - *.csv"))
    print(f"Found {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {f.name}")
    
    if not csv_files:
        print("ERROR: No CSV files found!")
        sys.exit(1)
    
    print("\nCreating converter...")
    converter = CSVConverter(csv_dir, output_dir)
    
    print("Running conversion...")
    converter.convert()
    
    print("\nConversion complete!")
    
except Exception as e:
    print(f"\nERROR: {e}")
    traceback.print_exc()
finally:
    log_file.close()
    print("\nLog written to csv_conversion_log.txt")
