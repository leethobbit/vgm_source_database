# Excel Column to Model Field Mapping Summary

## Quick Reference: Column Mappings

This document provides a quick reference for mapping Excel columns to Django model fields when converting `NEWER VGM Sound Sources.xlsx` to YAML fixtures.

---

## Tab Structure

- **First Tab**: "Rules" → **IGNORE**
- **All Other Tabs**: Game franchise names → **Become GameTags**

---

## Actual Structure: Game Titles + Sound Sources

**Row Organization**:
- Game titles appear as standalone rows
- All rows between game titles become sound sources for the previous game
- Section headers (like "Stuff to Find") are skipped
- Game description rows are skipped

### Game Title Rows

| Excel Column | Game Field | Type | Required | Notes |
|-------------|------------|------|----------|-------|
| First Column | `title` | CharField | ✅ Yes | Game title (e.g., "The Legend of Zelda: The Wind Waker") |
| *(Tab Name)* | `tags` | ManyToMany → GameTag | No | Tab name becomes the tag |
| *(Extracted)* | `release_year` | IntegerField | No | Extracted from parentheses in title (e.g., "(2002)") |

### Sound Source Rows (Between Game Titles)

| Excel Column Name | SoundSource Field | Type | Required | Notes |
|------------------|------------------|------|----------|-------|
| First Column | `name` | CharField | ✅ Yes | Sound source name (from first column) |
| `Bank` (if present) | `bank` | ForeignKey → Bank | ⚠️ Conditional | Either bank OR product required |
| `Product` (if present) | `product` | ForeignKey → Product | ⚠️ Conditional | Either bank OR product required |
| `Company` (if present) | → `product.company` | Indirect | No | Used to find/create Product |
| *(Auto-assigned)* | `games` | ManyToMany → Game | No | Automatically set to the previous game title |
| `Songs` (if present) | `songs` | ManyToMany → Song | No | Comma-separated song titles |
| Other Columns | `notes` | TextField | No | Additional information from other columns |
| *(Default)* | `discoverers` | ManyToMany → User | No | Empty `[]` for imports |

**Validation Rule**: At least one of `bank` OR `product` must be set (or will be created from company if available).

### Related Models (Created/Resolved During Conversion)

#### Company Model
- **Source**: `Company` column in Excel
- **Fields**: `name` (from Excel), `notes` (empty string)

#### Product Model
- **Source**: `Product` column in Excel
- **Fields**: `name` (from Excel), `company` (FK from Company column), `notes` (empty string)
- **Unique Constraint**: `(name, company)`

#### Bank Model
- **Source**: `Bank` column in Excel
- **Fields**: `name` (from Excel), `product` (FK from Product column), `notes` (empty string)
- **Unique Constraint**: `(name, product)`

#### Game Model (if referenced in Games column)
- **Source**: Parsed from `Games` column (comma-separated)
- **Fields**: `title` (from parsed value), `tags` (ManyToMany to GameTag from tab name), other fields default
- **Note**: Games may need to be created if they don't exist

#### Song Model (if referenced in Songs column)
- **Source**: Parsed from `Songs` column (comma-separated)
- **Fields**: `title` (from parsed value), `game` (FK - must resolve to Game), other fields default
- **Unique Constraint**: `(title, game)`

---

## Scenario 2: Rows are Games

### Game Model Mapping

| Excel Column Name | Game Field | Type | Required | Notes |
|------------------|------------|------|----------|-------|
| `Title` / `Game Title` | `title` | CharField | ✅ Yes | Primary identifier |
| `Release Date` | `release_date` | DateField | No | Format: YYYY-MM-DD |
| `Release Year` | `release_year` | IntegerField | No | Numeric year (e.g., 1995) |
| `Album Artists` / `Composers` | `album_artists` | ManyToMany → Person | No | Comma-separated names |
| `Notes` / `Description` | `notes` | TextField | No | Multi-line text |
| *(Tab Name)* | `tags` | ManyToMany → GameTag | No | Tab name becomes the tag |

### Related Models (Created/Resolved During Conversion)

#### Person Model (if referenced in Album Artists column)
- **Source**: Parsed from `Album Artists` / `Composers` column
- **Fields**: `name` (from parsed value), `notes` (empty string), `products` (empty list)

---

## Scenario 3: Rows Contain Both Games and SoundSources

If the Excel contains both Game and SoundSource data in the same row:

- **Game columns** → Create/update Game objects
- **SoundSource columns** → Create SoundSource objects
- **Link them** via the `games` ManyToMany field on SoundSource

---

## GameTag Model (From Tab Names)

### GameTag Mapping

| Source | GameTag Field | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| Tab name (e.g., "Final Fantasy") | `name` | CharField | ✅ Yes | Tab name becomes tag name |
| *(Auto-generated)* | `slug` | SlugField | Auto | Generated from name using slugify |
| *(Optional)* | `description` | TextField | No | Can be empty string |

**Example**:
- Tab: "Final Fantasy" → GameTag: `name="Final Fantasy"`, `slug="final-fantasy"`
- Tab: "Chrono Trigger" → GameTag: `name="Chrono Trigger"`, `slug="chrono-trigger"`

---

## YAML Output File Order

Generate YAML files in this dependency order:

1. **games_gametags.yaml** - All GameTags (from tab names)
2. **sources_companies.yaml** - All Companies (if referenced)
3. **sources_products.yaml** - All Products (if referenced)
4. **sources_banks.yaml** - All Banks (if referenced)
5. **songs_people.yaml** - All People/Artists (if referenced)
6. **games_games.yaml** - All Games (if present or referenced)
7. **songs_songs.yaml** - All Songs (if referenced)
8. **sources_soundsources.yaml** - All SoundSources

---

## Relationship Resolution Strategy

### ForeignKey Resolution

1. **Company**: Look up by `name` (unique)
2. **Product**: Look up by `(name, company)` (unique_together)
3. **Bank**: Look up by `(name, product)` (unique_together)
4. **Game**: Look up by `title` (may need to handle duplicates)
5. **Song**: Look up by `(title, game)` (unique_together)

### ManyToMany Resolution

1. Parse comma-separated values (e.g., "Game 1, Game 2, Game 3")
2. For each value:
   - Look up existing object
   - If not found, create new object (for Person, Game, Song)
   - Add to ManyToMany list as PK

### Example: Parsing "Games" Column

```
Excel: "Chrono Trigger, Final Fantasy VI"
→ Look up Game with title="Chrono Trigger" → PK: 1
→ Look up Game with title="Final Fantasy VI" → PK: 2
→ SoundSource.games = [1, 2]
```

---

## Field Value Formatting Rules

### Dates
- **Excel Format**: May vary (MM/DD/YYYY, DD/MM/YYYY, etc.)
- **YAML Format**: `YYYY-MM-DD` (e.g., `"1995-03-11"`)

### Empty Values
- **CharField/TextField with `blank=True`**: Use `""` (empty string), NOT `null`
- **ForeignKey with `null=True`**: Can use `null`
- **ManyToMany**: Use `[]` (empty list) if no relationships

### Multi-line Text
- Use YAML block scalar (`|` or `>`)

```yaml
notes: |
  First line of notes.
  
  Second line of notes.
```

---

## Next Steps

1. **Examine Excel Structure**: Run `examine_excel_structure.py` to see actual column names
2. **Verify Assumptions**: Confirm whether rows are SoundSources, Games, or both
3. **Create Conversion Script**: Based on actual Excel structure
4. **Generate YAML**: Create fixture files in dependency order
5. **Validate**: Run `python manage.py import_data --dry-run` to check for errors
6. **Import**: Run `python manage.py import_data` to import data

---

## Questions to Answer

Before creating the conversion script, determine:

1. ✅ What are the exact column names in the Excel file?
2. ✅ Do rows represent Games, SoundSources, or both?
3. ✅ How are relationships represented? (comma-separated, multiple columns, etc.)
4. ✅ What format are dates in? (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD, etc.)
5. ✅ Are there any existing Companies/Products/Banks in the database, or should they all be created?
6. ✅ How should duplicate names be handled? (e.g., multiple games with same title)
