# VGM Source Database - Import/Export Guide

This guide provides comprehensive documentation for importing and exporting data from the VGM Source Database using YAML fixtures.

## Table of Contents

1. [Overview](#overview)
2. [Management Commands](#management-commands)
3. [YAML Fixture Format](#yaml-fixture-format)
4. [Model-Specific Examples](#model-specific-examples)
5. [Field Value Handling](#field-value-handling)
6. [Relationship Handling](#relationship-handling)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Overview

The VGM Source Database uses Django's fixture system with YAML format for data import/export. This provides a human-readable, version-controllable way to manage database content.

### Key Features

- **Unified System**: Single import/export mechanism for all models
- **Dependency Handling**: Automatic ordering based on model relationships
- **YAML Format**: Human-readable and easy to edit
- **Validation**: Dry-run mode to validate before importing
- **Selective Export**: Export specific apps or all data

## Management Commands

### Export Data

Export all data to YAML fixtures:

```bash
python manage.py export_data
```

**Options:**
- `--output-dir DIR`: Specify output directory (default: `fixtures`)
- `--app APP_NAME`: Export only a specific app (`games`, `songs`, `sources`)
- `--format FORMAT`: Output format (`yaml` or `json`, default: `yaml`)

**Examples:**
```bash
# Export all data
python manage.py export_data

# Export only games app
python manage.py export_data --app games

# Export to custom directory
python manage.py export_data --output-dir my_fixtures

# Export as JSON
python manage.py export_data --format json
```

### Import Data

Import data from YAML fixtures:

```bash
python manage.py import_data
```

**Options:**
- `--fixture-dir DIR`: Directory containing fixtures (default: `fixtures`)
- `--file FILE`: Import a specific fixture file
- `--dry-run`: Validate fixtures without importing
- `--verbosity LEVEL`: Verbosity level (0-3)

**Examples:**
```bash
# Import all fixtures
python manage.py import_data

# Import from custom directory
python manage.py import_data --fixture-dir my_fixtures

# Import specific file
python manage.py import_data --file fixtures/games_games.yaml

# Validate without importing
python manage.py import_data --dry-run
```

## YAML Fixture Format

Django fixtures use a specific format where each object is represented as a dictionary with `model`, `pk`, and `fields` keys.

### Basic Structure

```yaml
- model: app_label.ModelName
  pk: 1
  fields:
    field_name: value
    another_field: value
```

### Key Points

- **model**: Full model path in format `app_label.ModelName`
- **pk**: Primary key (integer or string)
- **fields**: Dictionary of field values (excludes `pk`, `id`, and auto-generated fields)

## Model-Specific Examples

### Games App

#### GameTag

**Model**: `vgm_source_database.games.GameTag`

**Fields:**
- `name` (CharField, required, unique)
- `slug` (SlugField, auto-generated if not provided)
- `description` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Example:**
```yaml
- model: vgm_source_database.games.GameTag
  pk: 1
  fields:
    name: "Action"
    slug: "action"
    description: "Action-oriented games with fast-paced gameplay"

- model: vgm_source_database.games.GameTag
  pk: 2
  fields:
    name: "RPG"
    slug: "rpg"
    description: "Role-playing games"
```

#### Game

**Model**: `vgm_source_database.games.Game`

**Fields:**
- `title` (CharField, required)
- `release_date` (DateField, optional, format: YYYY-MM-DD)
- `release_year` (IntegerField, optional)
- `album_artists` (ManyToManyField to Person, optional)
- `tags` (ManyToManyField to GameTag, optional)
- `notes` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Example:**
```yaml
- model: vgm_source_database.games.Game
  pk: 1
  fields:
    title: "Chrono Trigger"
    release_date: "1995-03-11"
    release_year: 1995
    album_artists: [1, 2]  # Person PKs
    tags: [1, 2]  # GameTag PKs
    notes: |
      Classic JRPG with an iconic soundtrack.
      Composed by Yasunori Mitsuda and Nobuo Uematsu.

- model: vgm_source_database.games.Game
  pk: 2
  fields:
    title: "Final Fantasy VI"
    release_date: "1994-04-02"
    release_year: 1994
    tags: [2]  # RPG tag
    notes: ""
```

### Songs App

#### Person

**Model**: `vgm_source_database.songs.Person`

**Fields:**
- `name` (CharField, required)
- `products` (ManyToManyField to Product, optional)
- `notes` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Example:**
```yaml
- model: vgm_source_database.songs.Person
  pk: 1
  fields:
    name: "Yasunori Mitsuda"
    notes: "Japanese composer known for Chrono Trigger and Xenogears"

- model: vgm_source_database.songs.Person
  pk: 2
  fields:
    name: "Nobuo Uematsu"
    notes: "Composer of Final Fantasy series"
```

#### Song

**Model**: `vgm_source_database.songs.Song`

**Fields:**
- `title` (CharField, required)
- `game` (ForeignKey to Game, required)
- `composers` (ManyToManyField to Person, optional)
- `arrangers` (ManyToManyField to Person, optional)
- `track_number` (PositiveIntegerField, optional)
- `notes` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Unique Constraint**: `(title, game)` - songs must have unique titles per game

**Example:**
```yaml
- model: vgm_source_database.songs.Song
  pk: 1
  fields:
    title: "Chrono Trigger"
    game: 1  # Chrono Trigger game PK
    composers: [1]  # Yasunori Mitsuda
    arrangers: []
    track_number: 1
    notes: "Main theme of Chrono Trigger"

- model: vgm_source_database.songs.Song
  pk: 2
  fields:
    title: "Corridors of Time"
    game: 1  # Chrono Trigger game PK
    composers: [1]  # Yasunori Mitsuda
    track_number: 5
    notes: ""
```

### Sources App

#### Company

**Model**: `vgm_source_database.sources.Company`

**Fields:**
- `name` (CharField, required, unique)
- `notes` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Example:**
```yaml
- model: vgm_source_database.sources.Company
  pk: 1
  fields:
    name: "Roland Corporation"
    notes: "Japanese manufacturer of electronic musical instruments"

- model: vgm_source_database.sources.Company
  pk: 2
  fields:
    name: "Yamaha Corporation"
    notes: ""
```

#### Product

**Model**: `vgm_source_database.sources.Product`

**Fields:**
- `name` (CharField, required)
- `company` (ForeignKey to Company, required)
- `notes` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Unique Constraint**: `(name, company)` - products must have unique names per company

**Example:**
```yaml
- model: vgm_source_database.sources.Product
  pk: 1
  fields:
    name: "SC-55"
    company: 1  # Roland Corporation
    notes: "Sound Canvas 55, a popular MIDI sound module"

- model: vgm_source_database.sources.Product
  pk: 2
  fields:
    name: "SC-88"
    company: 1  # Roland Corporation
    notes: "Sound Canvas 88, successor to SC-55"
```

#### Bank

**Model**: `vgm_source_database.sources.Bank`

**Fields:**
- `name` (CharField, required)
- `product` (ForeignKey to Product, required)
- `notes` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Unique Constraint**: `(name, product)` - banks must have unique names per product

**Example:**
```yaml
- model: vgm_source_database.sources.Bank
  pk: 1
  fields:
    name: "Preset A"
    product: 1  # SC-55
    notes: "Default preset bank"

- model: vgm_source_database.sources.Bank
  pk: 2
  fields:
    name: "Preset B"
    product: 1  # SC-55
    notes: ""
```

#### SoundSource

**Model**: `vgm_source_database.sources.SoundSource`

**Fields:**
- `name` (CharField, required)
- `bank` (ForeignKey to Bank, optional, but either bank OR product required)
- `product` (ForeignKey to Product, optional, but either bank OR product required)
- `discoverers` (ManyToManyField to User, optional)
- `games` (ManyToManyField to Game, optional)
- `songs` (ManyToManyField to Song, optional)
- `notes` (TextField, optional)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-generated)

**Validation**: At least one of `bank` or `product` must be set

**Example:**
```yaml
- model: vgm_source_database.sources.SoundSource
  pk: 1
  fields:
    name: "Piano 1"
    bank: 1  # Preset A bank
    product: null  # Not needed when bank is set
    discoverers: []  # User PKs (if any)
    games: [1]  # Chrono Trigger
    songs: [1, 2]  # Multiple songs
    notes: |
      Classic piano sound used in Chrono Trigger.
      Identified in SC-55 Preset A bank.

- model: vgm_source_database.sources.SoundSource
  pk: 2
  fields:
    name: "Orchestra Hit"
    bank: null
    product: 1  # SC-55 (no specific bank)
    games: [1, 2]
    songs: []
    notes: ""
```

## Field Value Handling

### CharField and TextField

**Fields with `blank=True` but NOT `null=True`**: MUST use empty string `""`, NOT `null`

These fields allow blank values in forms but the database column does NOT allow NULL.

```yaml
# Correct
description: ""
notes: ""

# Incorrect - will cause database constraint violations
description: null
notes:  # Empty, parsed as null by YAML
```

### ForeignKey Fields

**Fields with `null=True` and `blank=True`**: CAN use `null` for empty values

```yaml
# Correct - null for optional ForeignKey
bank: null
product: null

# Also acceptable - empty string (but null is clearer)
bank: ""
```

**Fields without `null=True`**: MUST have a value (cannot be null)

```yaml
# Required ForeignKey - must have a value
game: 1  # Must reference existing Game PK
company: 2  # Must reference existing Company PK
```

### DateField

Use ISO format: `YYYY-MM-DD`

```yaml
release_date: "1995-03-11"
release_date: null  # If optional
```

### IntegerField

Use numeric values:

```yaml
release_year: 1995
track_number: 1
track_number: null  # If optional
```

### ManyToManyField

Use a list of primary keys:

```yaml
tags: [1, 2, 3]  # List of GameTag PKs
composers: [1]  # List of Person PKs
games: []  # Empty list if no relationships
```

### BooleanField

Use `true` or `false` (not `null`):

```yaml
is_active: true
is_published: false
```

### Multi-line Text Fields

Use YAML block scalar for multi-line text:

```yaml
notes: |
  First paragraph of notes.
  
  Second paragraph with more details.
  
  Third paragraph.
```

## Relationship Handling

### ForeignKey References

ForeignKeys reference objects by primary key:

```yaml
# Game references GameTag
- model: vgm_source_database.games.Game
  fields:
    title: "Example Game"
    tags: [1, 2]  # References GameTag PKs 1 and 2

# Song references Game
- model: vgm_source_database.songs.Song
  fields:
    title: "Example Song"
    game: 1  # References Game PK 1
```

### ManyToMany Relationships

ManyToMany fields are represented as lists of primary keys:

```yaml
# Game with multiple tags
- model: vgm_source_database.games.Game
  fields:
    title: "Chrono Trigger"
    tags: [1, 2, 3]  # Multiple GameTag PKs
    album_artists: [1, 2]  # Multiple Person PKs

# Song with composers and arrangers
- model: vgm_source_database.songs.Song
  fields:
    title: "Main Theme"
    game: 1
    composers: [1]  # Single composer
    arrangers: [2, 3]  # Multiple arrangers
```

### Dependency Order

When creating fixtures manually, respect this import order:

1. **GameTag** (no dependencies)
2. **Game** (depends on GameTag for tags)
3. **Person** (no dependencies)
4. **Song** (depends on Game and Person)
5. **Company** (no dependencies)
6. **Product** (depends on Company)
7. **Bank** (depends on Product)
8. **SoundSource** (depends on Bank, Product, Game, Song, User)

## Best Practices

### 1. Use Export Command

Always use the export command to generate initial fixtures:

```bash
python manage.py export_data
```

This ensures correct format and handles relationships properly.

### 2. Validate Before Import

Use dry-run mode to validate fixtures:

```bash
python manage.py import_data --dry-run
```

### 3. Version Control

Commit fixture files to version control for:
- Reproducible database states
- Sharing data between environments
- Backup and recovery

### 4. Incremental Updates

When updating fixtures:
1. Export current data
2. Make edits to YAML files
3. Test with dry-run
4. Import updated fixtures

### 5. Handle Relationships Carefully

- Ensure referenced objects exist (check PKs)
- Maintain referential integrity
- Use natural keys when possible (Django handles this automatically)

### 6. Field Value Rules

- **CharField/TextField with `blank=True`**: Use `""` not `null`
- **ForeignKey with `null=True`**: Can use `null`
- **Required fields**: Always provide values
- **ManyToMany**: Use lists `[1, 2, 3]` or empty lists `[]`

### 7. Test in Development First

Always test fixture imports in development before production:

```bash
# Development
python manage.py import_data --fixture-dir fixtures

# Verify data
python manage.py shell
>>> from vgm_source_database.games.models import Game
>>> Game.objects.count()
```

## Troubleshooting

### Common Errors

#### 1. "IntegrityError: null value in column violates not-null constraint"

**Cause**: Using `null` for a CharField/TextField that doesn't allow NULL.

**Solution**: Use empty string `""` instead of `null`.

```yaml
# Wrong
notes: null

# Correct
notes: ""
```

#### 2. "DoesNotExist: Game matching query does not exist"

**Cause**: Referencing a ForeignKey that doesn't exist.

**Solution**: Ensure referenced objects are created first, or use correct PKs.

```yaml
# Ensure Game with PK 1 exists before creating Song
- model: vgm_source_database.songs.Song
  fields:
    game: 1  # Must exist
```

#### 3. "IntegrityError: duplicate key value violates unique constraint"

**Cause**: Violating unique constraints (e.g., duplicate GameTag name, duplicate (title, game) for Song).

**Solution**: Check for duplicates and ensure uniqueness.

```yaml
# Wrong - duplicate name
- model: vgm_source_database.games.GameTag
  fields:
    name: "Action"  # Already exists

# Correct - unique name
- model: vgm_source_database.games.GameTag
  fields:
    name: "Action-Adventure"  # Different name
```

#### 4. "ValidationError: Sound source must have either a bank OR a product"

**Cause**: SoundSource requires at least one of `bank` or `product`.

**Solution**: Provide at least one:

```yaml
# Wrong - both null
- model: vgm_source_database.sources.SoundSource
  fields:
    bank: null
    product: null

# Correct - at least one set
- model: vgm_source_database.sources.SoundSource
  fields:
    bank: 1
    product: null
```

### Debugging Tips

1. **Use dry-run mode**:
   ```bash
   python manage.py import_data --dry-run
   ```

2. **Check YAML syntax**:
   ```bash
   python -c "import yaml; yaml.safe_load(open('fixtures/games_games.yaml'))"
   ```

3. **Import one file at a time**:
   ```bash
   python manage.py import_data --file fixtures/games_gametags.yaml
   ```

4. **Check database state**:
   ```bash
   python manage.py shell
   >>> from vgm_source_database.games.models import GameTag
   >>> GameTag.objects.all()
   ```

5. **Verify relationships**:
   ```bash
   python manage.py shell
   >>> from vgm_source_database.games.models import Game
   >>> game = Game.objects.get(pk=1)
   >>> game.tags.all()  # Check M2M relationships
   ```

## Additional Resources

- [Django Fixtures Documentation](https://docs.djangoproject.com/en/stable/howto/initial-data/)
- [YAML Syntax Guide](https://yaml.org/spec/1.2.2/)
- Project-specific rules: `.cursor/rules/general/import-file-creation.mdc`
