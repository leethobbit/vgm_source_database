# Fixtures Directory

This directory contains YAML fixture files for importing/exporting data from the VGM Source Database.

## Usage

### Export Data
```bash
python manage.py export_data
python manage.py export_data --output-dir fixtures
python manage.py export_data --app games
python manage.py export_data --format json
```

### Import Data
```bash
python manage.py import_data
python manage.py import_data --fixture-dir fixtures
python manage.py import_data --file fixtures/games_games.yaml
python manage.py import_data --dry-run  # Validate without importing
```

## File Naming Convention

Fixtures are named using the pattern: `{app}_{model_plural}.yaml`

- `games_gametags.yaml` - Game tags
- `games_games.yaml` - Games
- `songs_people.yaml` - People (composers, arrangers, etc.)
- `songs_songs.yaml` - Songs
- `sources_companies.yaml` - Companies
- `sources_products.yaml` - Products
- `sources_banks.yaml` - Banks
- `sources_soundsources.yaml` - Sound sources

## Import Order

When importing, fixtures are loaded in dependency order:
1. Game Tags (no dependencies)
2. Games (depends on Game Tags)
3. People (no dependencies)
4. Songs (depends on Games and People)
5. Companies (no dependencies)
6. Products (depends on Companies)
7. Banks (depends on Products)
8. Sound Sources (depends on Banks, Products, Games, Songs, Users)

See `ai_docs/IMPORT_EXPORT_GUIDE.md` for detailed documentation and examples.
