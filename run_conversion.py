"""Run the conversion script with explicit error handling."""
import sys
import traceback
from pathlib import Path

try:
    from convert_excel_to_yaml import ExcelConverter
    
    excel_file = Path("dev_reference/NEWER VGM Sound Sources.xlsx")
    output_dir = "fixtures"
    
    print(f"Checking for file: {excel_file}")
    print(f"File exists: {excel_file.exists()}")
    
    if not excel_file.exists():
        print(f"ERROR: File not found: {excel_file}")
        sys.exit(1)
    
    print(f"Creating converter...")
    converter = ExcelConverter(str(excel_file), output_dir)
    
    print(f"Starting conversion...")
    converter.convert()
    
    print("Done!")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
