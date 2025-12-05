# Excel to YAML Conversion Instructions

## Scripts Available

1. **`convert_excel_to_yaml.py`** - Main conversion script (recommended)
2. **`final_convert.py`** - Alternative script with file-based status reporting
3. **`simple_convert.py`** - Simplified version

## How to Run

```bash
# From the project root directory
python convert_excel_to_yaml.py
```

Or:

```bash
python final_convert.py
```

## Expected Output

The script will:
1. Process all sheets (except "Rules")
2. Create GameTags from sheet names
3. Identify game title rows
4. Group rows between game titles as sound sources
5. Generate YAML files in `fixtures/` directory:
   - `games_gametags.yaml`
   - `sources_companies.yaml`
   - `sources_products.yaml`
   - `sources_banks.yaml`
   - `games_games.yaml`
   - `sources_soundsources.yaml`
6. Create `skipped_lines_report.txt` with all skipped lines

## What the Script Does

### Game Title Detection
- Identifies standalone rows with game titles (10+ characters)
- Looks for indicators: colons, parentheses, platform names (Wii, PlayStation, etc.)
- Extracts release year from parentheses (e.g., "(2002)")

### Sound Source Grouping
- All rows between game titles become sound sources for the previous game
- First column becomes the sound source name
- Maps other columns to Bank, Product, Company, Notes

### Smart Skipping
- Skips section headers ("Stuff to Find", "Sources", etc.)
- Skips empty rows
- Skips rows that don't parse as sound sources
- Tracks all skipped lines with reasons

## Validation

After conversion, validate the YAML files:

```bash
python manage.py import_data --dry-run
```

This will check for errors without importing.

## Import

Once validated:

```bash
python manage.py import_data
```

## Troubleshooting

If the script doesn't produce output:
1. Check that `openpyxl` and `pyyaml` are installed: `pip install openpyxl pyyaml`
2. Verify the Excel file exists at `dev_reference/NEWER VGM Sound Sources.xlsx`
3. Check that the `fixtures/` directory exists and is writable
4. Run with explicit Python: `python -u convert_excel_to_yaml.py`
5. Check for error messages in the console

## Manual Conversion (If Script Fails)

If the automated script fails, you can manually convert following these rules:

1. **For each sheet (except "Rules")**:
   - Create a GameTag with the sheet name

2. **For each game title row**:
   - Create a Game with:
     - `title`: The game title text
     - `tags`: The GameTag from the sheet name
     - `release_year`: Extract from parentheses if present
     - Other fields: empty/default

3. **For each row between game titles**:
   - Create a SoundSource with:
     - `name`: First column value
     - `games`: The previous game title
     - `bank`: From "Bank" column (if present)
     - `product`: From "Product" column (if present)
     - `company`: From "Company" column (if present)
     - `notes`: From "Notes" or "Description" columns
   - Skip section headers and invalid rows

4. **Create supporting objects**:
   - Companies: From "Company" column values
   - Products: From "Product" column (linked to Company)
   - Banks: From "Bank" column (linked to Product)

5. **Generate YAML files in dependency order**:
   - GameTags first
   - Companies
   - Products
   - Banks
   - Games
   - SoundSources

See `ai_docs/COLUMN_MAPPING_SUMMARY.md` for detailed field mappings.
