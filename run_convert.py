"""Run conversion with explicit output."""
import sys
import traceback

# Force output
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

try:
    print("Starting conversion...", flush=True)
    
    from pathlib import Path
    from convert_excel_to_yaml import ExcelConverter
    
    excel_file = Path("dev_reference/NEWER VGM Sound Sources.xlsx")
    output_dir = "fixtures"
    
    print(f"Excel file: {excel_file}", flush=True)
    print(f"Exists: {excel_file.exists()}", flush=True)
    
    if not excel_file.exists():
        print(f"ERROR: File not found: {excel_file}", flush=True)
        sys.exit(1)
    
    print("Creating converter...", flush=True)
    converter = ExcelConverter(str(excel_file), output_dir)
    
    print("Running conversion...", flush=True)
    converter.convert()
    
    print("Conversion complete!", flush=True)
    
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)
