# CSV to YAML Conversion Guide

This guide explains how to convert the `all_fixtures.csv` file into YAML fixture format.

## CSV Structure

The CSV file contains all fixture data in a single file with the following columns:

### Common Columns
- `model`: The full model path (e.g., `vgm_source_database.games.Game`)
- `pk`: Primary key (integer)
- `notes`: Text field (may contain `\n` for newlines)

### Model-Specific Columns

#### GameTag
- `name`: Tag name
- `slug`: URL-friendly slug
- `description`: Tag description

#### Company
- `name`: Company name

#### Product
- `name`: Product name
- `company`: Foreign key to Company (integer PK)

#### Bank
- `name`: Bank name
- `product`: Foreign key to Product (integer PK)

#### Person
- `name`: Person name
- `products`: Many-to-many field - pipe-separated Product PKs (e.g., `1|2|3`)

#### Game
- `title`: Game title
- `release_date`: Date in YYYY-MM-DD format
- `release_year`: Year (integer)
- `album_artists`: Many-to-many field - pipe-separated Person PKs
- `tags`: Many-to-many field - pipe-separated GameTag PKs

#### Song
- `title`: Song title
- `game`: Foreign key to Game (integer PK)
- `track_number`: Track number (integer)
- `composers`: Many-to-many field - pipe-separated Person PKs
- `arrangers`: Many-to-many field - pipe-separated Person PKs

#### SoundSource
- `name`: Sound source name
- `bank`: Foreign key to Bank (integer PK, nullable)
- `product`: Foreign key to Product (integer PK, nullable)
- `discoverers`: Many-to-many field - pipe-separated User PKs
- `games`: Many-to-many field - pipe-separated Game PKs
- `songs`: Many-to-many field - pipe-separated Song PKs

## Conversion Rules

### 1. Empty Fields
- Empty CSV cells should be converted to `null` in YAML (for nullable fields) or omitted (for required fields)
- Empty strings (`""`) should be converted to empty string `""` in YAML

### 2. Many-to-Many Fields
- Pipe-separated values (e.g., `1|2|3`) should be converted to YAML lists: `[1, 2, 3]`
- Empty M2M fields should be converted to empty lists: `[]`

### 3. Multi-line Notes
- Newlines in CSV are represented as `\n` escape sequences
- Convert `\n` to actual newlines in YAML, using the `|` literal block scalar for multi-line content
- Single-line notes can use regular YAML strings

### 4. Foreign Keys
- Foreign key fields contain integer PKs
- Convert directly to integers in YAML
- `null` values should be represented as `null` in YAML

## Example Conversion

### CSV Row:
```csv
vgm_source_database.games.Game,1,,,Chrono Trigger,1995-03-11,1995,,,,,1|2,1|2,,,,,"Classic JRPG with an iconic soundtrack.\nComposed by Yasunori Mitsuda and Nobuo Uematsu."
```

### YAML Output:
```yaml
- model: vgm_source_database.games.Game
  pk: 1
  fields:
    title: "Chrono Trigger"
    release_date: "1995-03-11"
    release_year: 1995
    album_artists: [1, 2]
    tags: [1, 2]
    notes: |
      Classic JRPG with an iconic soundtrack.
      Composed by Yasunori Mitsuda and Nobuo Uematsu.
```

## Conversion Script

You can use the following Python script to convert CSV to YAML:

```python
import csv
import yaml

def csv_to_yaml(csv_file, yaml_file):
    fixtures = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Build the fixture entry
            fixture = {
                'model': row['model'],
                'pk': int(row['pk']),
                'fields': {}
            }
            
            # Process each field
            for key, value in row.items():
                if key in ['model', 'pk']:
                    continue
                
                if not value or value.strip() == '':
                    continue
                
                # Handle many-to-many fields (pipe-separated)
                m2m_fields = ['album_artists', 'tags', 'composers', 'arrangers', 
                             'discoverers', 'games', 'songs', 'products']
                if key in m2m_fields:
                    if value:
                        fixture['fields'][key] = [int(x) for x in value.split('|')]
                    else:
                        fixture['fields'][key] = []
                # Handle foreign keys
                elif key in ['company', 'product', 'bank', 'game']:
                    if value:
                        fixture['fields'][key] = int(value)
                    else:
                        fixture['fields'][key] = None
                # Handle integer fields
                elif key in ['release_year', 'track_number']:
                    fixture['fields'][key] = int(value)
                # Handle notes with newlines
                elif key == 'notes' and '\\n' in value:
                    fixture['fields'][key] = value.replace('\\n', '\n')
                # Handle regular string fields
                else:
                    fixture['fields'][key] = value
            
            fixtures.append(fixture)
    
    # Write YAML file
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(fixtures, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"Converted {len(fixtures)} fixtures to {yaml_file}")

# Usage
csv_to_yaml('all_fixtures.csv', 'all_fixtures.yaml')
```

## Notes

- The CSV file should be saved with UTF-8 encoding
- Foreign key references must use PKs that exist in the database
- Many-to-many relationships should reference existing PKs
- The order of rows matters for dependencies (e.g., Companies before Products, Products before Banks)

