# Excel to YAML Conversion Plan
## NEWER VGM Sound Sources.xlsx

This document outlines the plan for converting the Excel file `NEWER VGM Sound Sources.xlsx` to YAML fixture format for import into the VGM Source Database.

## Overview

**Source File**: `dev_reference/NEWER VGM Sound Sources.xlsx`

**Structure**:
- **First Tab**: "Rules" (to be ignored)
- **Remaining Tabs**: Named after popular video game franchises (e.g., "Final Fantasy", "Chrono Trigger", "Mario", etc.)
- **Tab Purpose**: Each tab represents a GameTag category
- **Row Structure**: 
  - **Game Title Rows**: Standalone rows containing game titles (e.g., "The Legend of Zelda: The Wind Waker")
  - **Sound Source Rows**: All rows between game titles represent sound sources for the previous game
  - **Section Headers**: Rows like "Stuff to Find" that organize sound sources (to be skipped)
  - **Description Rows**: Rows between game title and sound sources that describe the game (to be skipped)

## Structure Details

1. **Tabs = GameTags**: Each tab name (except "Rules") will become a GameTag
2. **Game Title Rows**: 
   - Appear as standalone rows with game titles in the first column
   - Examples: "The Legend of Zelda: The Wind Waker", "The Legend of Zelda: The Wind Waker HD (Nintendo Wii U)"
   - May contain release year in parentheses
   - Other columns are typically empty
3. **Sound Source Rows**: 
   - All rows between game titles become sound sources for the previous game
   - First column typically contains the sound source name
   - May contain Bank, Product, Company information in other columns
4. **Rows to Skip**:
   - Section headers (e.g., "Stuff to Find")
   - Game description rows (between game title and first sound source)
   - Empty rows
   - Rows that don't make sense as sound sources

## Expected Column Mappings

Based on the model structure, here are the likely column mappings:

### If Rows Represent SoundSources

| Excel Column | SoundSource Field | Model Field Type | Notes |
|-------------|-------------------|------------------|-------|
| Name / Sound Name | `name` | CharField (required) | Primary identifier |
| Bank | `bank` | ForeignKey to Bank (optional) | Must resolve to existing Bank |
| Product | `product` | ForeignKey to Product (optional) | Must resolve to existing Product |
| Company | → Product → Company | Indirect | Used to find/create Product |
| Games | `games` | ManyToMany to Game | Comma-separated or multiple columns |
| Songs | `songs` | ManyToMany to Song | Comma-separated or multiple columns |
| Notes / Description | `notes` | TextField (optional) | Multi-line text |
| Discoverers | `discoverers` | ManyToMany to User (optional) | Usually empty for imports |

**Validation**: At least one of `bank` OR `product` must be set.

### If Rows Represent Games

| Excel Column | Game Field | Model Field Type | Notes |
|-------------|------------|------------------|-------|
| Title / Game Title | `title` | CharField (required) | Primary identifier |
| Release Date | `release_date` | DateField (optional) | Format: YYYY-MM-DD |
| Release Year | `release_year` | IntegerField (optional) | Numeric year |
| Album Artists | `album_artists` | ManyToMany to Person | Comma-separated names |
| Notes | `notes` | TextField (optional) | Multi-line text |
| Tag | `tags` | ManyToMany to GameTag | Tab name becomes the tag |

### If Rows Represent Both (Mixed Data)

The Excel might contain a mix where:
- Some columns identify the Game
- Other columns identify the SoundSource
- The tab name provides the GameTag context

## Conversion Process

### Step 1: Extract Tab Information

1. **Skip "Rules" tab**
2. **For each remaining tab**:
   - Tab name → GameTag name
   - Create GameTag entry (if doesn't exist)
   - Process all rows in the tab

### Step 2: Identify Data Type

Examine the first data row to determine:
- Are we looking at SoundSource data? (columns like "Bank", "Product", "Sound Name")
- Are we looking at Game data? (columns like "Title", "Release Date")
- Are we looking at mixed data? (both types of columns)

### Step 3: Map Columns to Fields

For each row:
1. **Read column headers** (first row of each tab)
2. **Map to model fields** based on the table above
3. **Handle relationships**:
   - ForeignKeys: Resolve to existing objects or create new ones
   - ManyToMany: Parse comma-separated values or multiple columns

### Step 4: Generate YAML Files

Create separate YAML files following the import order:

1. **games_gametags.yaml** - All GameTags from tab names
2. **games_games.yaml** - All Games (if present in Excel)
3. **songs_people.yaml** - All People/Artists (if referenced)
4. **songs_songs.yaml** - All Songs (if present in Excel)
5. **sources_companies.yaml** - All Companies (if referenced)
6. **sources_products.yaml** - All Products (if referenced)
7. **sources_banks.yaml** - All Banks (if referenced)
8. **sources_soundsources.yaml** - All SoundSources

## Detailed Field Mappings

### GameTag Model
- **Source**: Tab name (excluding "Rules")
- **Fields**:
  - `name`: Tab name (e.g., "Final Fantasy", "Chrono Trigger")
  - `slug`: Auto-generated from name (slugify)
  - `description`: Optional, could be empty string

### Game Model (if present)
- **Source**: Row data in tabs
- **Fields**:
  - `title`: From "Title" or "Game Title" column
  - `release_date`: From "Release Date" column (parse to YYYY-MM-DD)
  - `release_year`: From "Release Year" column (integer)
  - `album_artists`: From "Album Artists" or "Composers" column (parse names, create/link Person objects)
  - `tags`: Tab name (link to GameTag created from tab)
  - `notes`: From "Notes" or "Description" column

### SoundSource Model (if present)
- **Source**: Row data in tabs
- **Fields**:
  - `name`: From "Name", "Sound Name", or "Patch Name" column
  - `bank`: From "Bank" column (resolve to Bank object by name+product)
  - `product`: From "Product" column (resolve to Product object by name+company)
  - `games`: From "Games" column (comma-separated game titles, resolve to Game objects)
  - `songs`: From "Songs" column (comma-separated song titles, resolve to Song objects)
  - `notes`: From "Notes" or "Description" column
  - `discoverers`: Usually empty `[]` for imports

### Person Model (if referenced)
- **Source**: Parsed from "Album Artists", "Composers", "Arrangers" columns
- **Fields**:
  - `name`: Parsed name
  - `notes`: Optional, empty string
  - `products`: Usually empty `[]` for imports

### Company Model (if referenced)
- **Source**: From "Company" column
- **Fields**:
  - `name`: Company name (e.g., "Roland", "Yamaha")
  - `notes`: Optional, empty string

### Product Model (if referenced)
- **Source**: From "Product" column
- **Fields**:
  - `name`: Product name (e.g., "SC-55", "SC-88")
  - `company`: ForeignKey to Company (from "Company" column)
  - `notes`: Optional, empty string

### Bank Model (if referenced)
- **Source**: From "Bank" column
- **Fields**:
  - `name`: Bank name (e.g., "Preset A", "GM")
  - `product`: ForeignKey to Product (from "Product" column)
  - `notes`: Optional, empty string

## Relationship Resolution

### ForeignKey Resolution
- **Company**: Look up by `name` (unique)
- **Product**: Look up by `(name, company)` (unique_together)
- **Bank**: Look up by `(name, product)` (unique_together)
- **Game**: Look up by `title` (may need to handle duplicates)
- **Song**: Look up by `(title, game)` (unique_together)

### ManyToMany Resolution
- Parse comma-separated values or multiple columns
- For each value:
  - Look up existing object
  - If not found, create new object (for Person, Game, Song)
  - Add to ManyToMany list

## Implementation Steps

1. **Examine Excel Structure**
   - Read all sheet names
   - Read headers from first game sheet
   - Identify column types and data structure

2. **Create Conversion Script**
   - Use `openpyxl` or `pandas` to read Excel
   - Map columns to model fields
   - Generate YAML fixtures

3. **Handle Dependencies**
   - Create objects in dependency order:
     1. GameTags (from tab names)
     2. Companies
     3. Products
     4. Banks
     5. People
     6. Games
     7. Songs
     8. SoundSources

4. **Validate Output**
   - Check YAML syntax
   - Verify relationships
   - Use `import_data --dry-run` to validate

## Next Steps

1. **Examine Actual Excel File Structure**
   - Run script to read headers and sample rows
   - Identify exact column names
   - Determine if rows are Games, SoundSources, or both

2. **Create Conversion Script**
   - Based on actual structure
   - Handle edge cases (missing data, duplicates, etc.)
   - Generate YAML files

3. **Test Import**
   - Run `import_data --dry-run` on generated YAML
   - Fix any issues
   - Import actual data

## Questions to Resolve

1. What are the exact column names in the Excel file?
2. Do rows represent Games, SoundSources, or both?
3. How are relationships represented? (comma-separated, multiple columns, etc.)
4. Are there any existing Companies/Products/Banks in the database, or should they all be created?
5. How should duplicate names be handled? (e.g., multiple games with same title)
6. What format are dates in? (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD, etc.)

## Notes

- This plan is based on assumptions about the Excel structure
- Actual column mappings may differ
- The conversion script should be flexible to handle variations
- Consider creating a mapping configuration file for easy adjustments
