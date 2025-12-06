# Changelog - LLM Changes

## 2024-12-19 - Created Excel to YAML Conversion Plan

**Created Files:**
- `ai_docs/EXCEL_TO_YAML_CONVERSION_PLAN.md` - Comprehensive conversion plan document
  - Detailed mapping of Excel columns to Django model fields
  - Covers all scenarios (SoundSources, Games, or both)
  - Includes relationship resolution strategies
  - Documents dependency order for YAML generation
- `ai_docs/COLUMN_MAPPING_SUMMARY.md` - Quick reference for column mappings
  - Table format showing Excel columns → Model fields
  - Field type and requirement information
  - Relationship resolution examples
  - Field value formatting rules
- `examine_excel_structure.py` - Script to analyze Excel file structure
  - Reads sheet names and headers
  - Extracts sample data rows
  - Outputs JSON analysis for conversion script development
- `test_excel.py` - Test script for Excel examination

**Key Features:**
- **Tab Structure**: Each tab (except "Rules") becomes a GameTag
- **Column Mappings**: Detailed mappings for SoundSource and Game models
- **Relationship Handling**: Strategies for resolving ForeignKeys and ManyToMany fields
- **YAML Generation Order**: Proper dependency order for fixture files
- **Field Formatting**: Rules for dates, empty values, and multi-line text

**Next Steps:**
1. Run examination script to identify actual Excel structure
2. Create conversion script based on actual column names
3. Generate YAML fixtures following dependency order
4. Validate with dry-run before importing

## 2024-12-19 - Created Excel to YAML Conversion Script

**Created Files:**
- `convert_excel_to_yaml.py` - Main conversion script
  - Identifies game title rows (standalone rows with game titles)
  - Groups all rows between game titles as sound sources for the previous game
  - Skips section headers (like "Stuff to Find") and invalid rows
  - Tracks all skipped lines with reasons and sheet names
  - Generates YAML fixtures in proper dependency order
  - Creates skipped lines report (`skipped_lines_report.txt`)

**Modified Files:**
- `ai_docs/EXCEL_TO_YAML_CONVERSION_PLAN.md` - Updated with actual structure details
  - Documented game title row structure
  - Documented sound source grouping logic
  - Updated row organization explanation
- `ai_docs/COLUMN_MAPPING_SUMMARY.md` - Updated with correct mappings
  - Changed from "Scenario 1" to "Actual Structure"
  - Updated to reflect game title rows + sound source rows organization
  - Corrected field mappings based on actual structure

**Key Features:**
- **Game Title Detection**: Identifies standalone rows with game titles (10+ chars, contains game indicators)
- **Sound Source Grouping**: All rows between game titles automatically assigned to previous game
- **Smart Skipping**: Skips section headers, empty rows, and invalid rows
- **Relationship Resolution**: Automatically resolves ForeignKeys (Company, Product, Bank, Game)
- **Skipped Lines Tracking**: Tracks all skipped lines with reasons and generates report

**Structure Understanding:**
- Game titles appear as standalone rows (e.g., "The Legend of Zelda: The Wind Waker")
- All rows between game titles become sound sources for the previous game
- Section headers (like "Stuff to Find") are skipped
- Game description rows are skipped
- Invalid/unparseable rows are tracked and reported

**Usage:**
```bash
python convert_excel_to_yaml.py
```

**Output:**
- YAML fixture files in `fixtures/` directory:
  - `games_gametags.yaml`
  - `sources_companies.yaml`
  - `sources_products.yaml`
  - `sources_banks.yaml`
  - `games_games.yaml`
  - `sources_soundsources.yaml`
- `skipped_lines_report.txt` - Report of all skipped lines with reasons


## 2024-12-19 - Created Unified Import/Export System for YAML Fixtures

**Created Files:**
- `config/management/__init__.py` - Management commands package
- `config/management/commands/__init__.py` - Commands package
- `config/management/commands/export_data.py` - Export command implementation
  - Exports all models to YAML fixtures
  - Supports filtering by app, custom output directory, and format selection
  - Handles model dependencies and export ordering
- `config/management/commands/import_data.py` - Import command implementation
  - Imports data from YAML fixtures
  - Supports dry-run mode for validation
  - Handles dependency ordering automatically
- `ai_docs/IMPORT_EXPORT_GUIDE.md` - Comprehensive import/export documentation
  - Complete guide for all model types
  - Field value handling rules
  - Relationship handling examples
  - Best practices and troubleshooting
- `fixtures/.gitkeep` - Fixtures directory placeholder
- `fixtures/README.md` - Fixtures directory documentation
- `fixtures/examples/games_gametags.yaml` - Example GameTag fixtures
- `fixtures/examples/games_games.yaml` - Example Game fixtures
- `fixtures/examples/songs_people.yaml` - Example Person fixtures
- `fixtures/examples/songs_songs.yaml` - Example Song fixtures
- `fixtures/examples/sources_companies.yaml` - Example Company fixtures
- `fixtures/examples/sources_products.yaml` - Example Product fixtures
- `fixtures/examples/sources_banks.yaml` - Example Bank fixtures
- `fixtures/examples/sources_soundsources.yaml` - Example SoundSource fixtures

**Modified Files:**
- `.cursor/rules/general/import-file-creation.mdc`
  - Updated with VGM Source Database-specific examples
  - Added model-specific field handling rules
  - Added management command usage examples
  - Updated to reference project-specific documentation

**Key Features:**
- **Unified System**: Single import/export mechanism for all models
- **YAML Format**: Human-readable, version-controllable fixture format
- **Dependency Handling**: Automatic ordering based on model relationships
- **Validation**: Dry-run mode to validate fixtures before importing
- **Selective Export**: Export specific apps or all data
- **Comprehensive Documentation**: Complete guide with examples for each model type

**Model Coverage:**
- Games App: GameTag, Game
- Songs App: Person, Song
- Sources App: Company, Product, Bank, SoundSource

**Usage:**
```bash
# Export all data
python manage.py export_data

# Export specific app
python manage.py export_data --app games

# Import all fixtures
python manage.py import_data

# Validate without importing
python manage.py import_data --dry-run
```

**Result:**
- Complete import/export system for data migration
- Easy-to-use management commands
- Comprehensive documentation for all model types
- Example fixtures demonstrating proper format and relationships
- Version-controllable data management

## 2024-12-19 - Updated Navbar App Name

## 2024-12-19 - Updated Navbar App Name

**Modified Files:**
- `vgm_source_database/templates/base.html`
  - Updated navbar link text from "VGM Source Database" to "The VGM Sound Source Database"
  - Updated default page title to match for consistency

**Key Changes:**
- Changed app name in navbar to be more explicit about the database's purpose
- Both navbar link and page title now use "The VGM Sound Source Database"
- Improves clarity that the database focuses on sound sources

**Result:**
- Navbar displays more descriptive app name
- Consistent naming across navbar and page titles

## 2024-12-19 - Reordered Dashboard Statistics Blocks

**Modified Files:**
- `vgm_source_database/templates/pages/home.html`
  - Reordered statistics blocks within the grid layout
  - First row: Sound Sources, Games, Songs
  - Second row: Products, Companies, People

**Key Changes:**
- Changed order of statistics cards to match user requirements
- Grid layout automatically creates two rows with 3 columns each on large screens
- All functionality, links, and styling remain unchanged

**Result:**
- Dashboard statistics now display in the requested order
- Improved visual organization of statistics blocks

## 2024-12-19 - Fixed GameTag URL Pattern Ordering

**Modified Files:**
- `vgm_source_database/games/urls.py`
  - Reordered URL patterns to place `tags/create/` before `tags/<slug:slug>/`
  - Prevents "create" from being matched as a slug parameter
  - More specific patterns now come before general patterns (Django best practice)

**Key Changes:**
- Moved `path("tags/create/", ...)` before `path("tags/<slug:slug>/", ...)`
- Fixes 404 error when accessing tag creation page
- Django matches URL patterns in order, so specific patterns must come first

**Result:**
- Tag creation URL now works correctly
- URL routing follows Django best practices

## 2024-12-19 - Added Tag CRUD Views, Dashboard Button, and Sidebar with Top Categories

**Modified Files:**
- `vgm_source_database/templates/pages/home.html`
  - Added "Create Tag" button to Quick Actions section
  - Button uses `btn-success` class and links to `games:gametag_create`

- `vgm_source_database/games/context_processors.py` (new file)
  - Created context processor `top_categories()` to provide top game tags
  - Annotates tags with `game_count` using Django's `Count` aggregation
  - Filters tags with at least one game (`game_count__gt=0`)
  - Orders by game count descending and limits to top 20 tags

- `config/settings/base.py`
  - Added `vgm_source_database.games.context_processors.top_categories` to `TEMPLATES` context processors list
  - Makes top categories available in all templates

- `vgm_source_database/templates/base.html`
  - Restructured layout to include sidebar alongside main content
  - Added sidebar with fixed width (w-64) and sticky positioning
  - Sidebar includes "Top Categories" section showing tags sorted by occurrence count
  - Each tag displays name and game count in parentheses
  - Tags are clickable links to tag detail pages
  - Main content area now uses flexbox layout with sidebar on left
  - Sidebar uses dark theme styling consistent with navbar

**Key Changes:**
- CRUD views for GameTag already existed, so no changes needed to views/URLs
- Added "Create Tag" button to dashboard for quick access
- Created context processor to efficiently query top tags with game counts
- Added sidebar that sits outside main content window (similar to navbar)
- Sidebar displays "Top Categories" with tags sorted by most occurrences
- Tags show occurrence count in parentheses for easy reference
- Sidebar is sticky and remains visible when scrolling

**Result:**
- Easy access to tag creation from dashboard
- Sidebar provides quick navigation to popular tags
- Visual indication of tag popularity through occurrence counts
- Consistent dark theme styling throughout
- Improved navigation and discoverability of content

## 2024-12-19 - Converted Games Detail Page Songs List to Table with Sources

**Modified Files:**
- `vgm_source_database/games/views.py`
  - Updated `GameDetailView` to use `prefetch_related` for optimized querying
  - Added prefetching for `songs__sound_sources`, `tags`, and `album_artists`
  - Prevents N+1 queries when accessing sound sources for each song

- `vgm_source_database/templates/games/game_detail.html`
  - Replaced songs list with a table layout
  - First column displays songs (clickable links to song detail pages)
  - Second column displays sound sources for each song (clickable links to source detail pages)
  - Sources are displayed as comma-separated links
  - Empty state shows "-" when a song has no sources
  - Table uses consistent styling matching other list views in the project

**Key Changes:**
- Songs section now displays as a table instead of a vertical list
- Each song row shows the song name (with track number if available) in the first column
- Second column shows all sound sources linked to that song
- Both songs and sources are clickable links to their respective detail pages
- Improved performance with prefetch_related to avoid N+1 query issues
- Consistent table styling with other list views (song_list, etc.)

**Result:**
- Better organization of song and source information
- Easy navigation to both song and source detail pages
- Improved query performance when loading game detail pages
- Consistent UI/UX with other table views in the application

## 2024-12-19 - Fixed Recent History Duplicate Entries on Object Creation

**Modified Files:**
- `vgm_source_database/views.py`
  - Fixed issue where newly created objects appeared twice in Recent History (once as "Created" and once as "Updated")
  - Added tracking of objects already added as "Created" using a set of URLs
  - Updated `add_activity_items()` helper function to exclude objects from "Updated" list if they were already added as "Created"
  - Ensures each object only appears once in Recent History when first created

**Key Changes:**
- Introduced `created_urls` set to track URLs of objects added as "Created"
- Modified update logic to skip objects whose URLs are already in `created_urls`
- Prevents duplicate entries for newly created objects

## 2024-12-19 - Fixed SoundSource Validation to Allow Both Product and Bank

**Modified Files:**
- `vgm_source_database/sources/models.py`
  - Updated `SoundSource.clean()` method to allow both product and bank to be set
  - Removed validation that prevented both bank and product from being set
  - Updated docstring to reflect new validation rules
  - Sound sources can now have:
    - A product only (no bank)
    - Both a product and a bank (since banks are part of products)

**Key Changes:**
- Removed the check that raised an error when both bank and product were set
- Kept the check that ensures at least one of bank or product is set
- Updated validation logic to match business requirements where banks can be part of products

## 2024-12-19 - Switched to Tailwind CSS Play CDN for Testing

**Modified Files:**
- `vgm_source_database/templates/base.html`
  - Replaced static CSS file with Tailwind CSS Play CDN script
  - Added inline `<style type="text/tailwindcss">` block with custom theme and components
  - Defined all custom neon color classes and component styles
  - Converted @apply directives to regular CSS for Play CDN compatibility

**Key Changes:**
- Using Tailwind CSS v4 Play CDN (`@tailwindcss/browser@4`) for instant styling without build step
- All custom neon colors and components defined inline
- No build process required - works immediately for testing
- Homepage and all templates verified to use Tailwind classes correctly

**Note:** Play CDN is for development/testing. For production, switch back to compiled CSS.

## 2024-12-19 - Converted All Templates to Tailwind CSS and Alpine.js

**Modified Files:**
- All list templates (game_list, song_list, person_list, company_list, product_list, bank_list, soundsource_list, gametag_list)
- All detail templates (game_detail, song_detail, person_detail, company_detail, product_detail, bank_detail, soundsource_detail, gametag_detail)
- All form templates (game_form, song_form, person_form, company_form, product_form, bank_form, soundsource_form, gametag_form)
- User templates (user_detail, user_form)
- Home page template (already converted)

**Key Changes:**
- Replaced all Bootstrap classes with Tailwind CSS utility classes
- Used custom Tailwind components (`.card-neon`, `.btn-success`, `.btn-primary`, etc.) for retro neon styling
- Maintained backward compatibility with button class names
- All templates now use consistent retro neon aesthetic with dark theme
- Updated Dockerfile to build Tailwind CSS during container build

**Docker Integration:**
- `compose/local/django/Dockerfile` - Added Node.js installation and CSS build step

## 2024-12-19 - Switched Theme to Tailwind CSS with Dark Retro Neon Colors

**Created Files:**
- `package.json` - npm configuration with Tailwind CSS dependencies and build scripts
- `tailwind.config.js` - Tailwind configuration with dark theme and retro neon color palette
- `postcss.config.js` - PostCSS configuration for Tailwind processing
- `vgm_source_database/static/css/input.css` - Tailwind source file with custom retro neon theme styles

**Modified Files:**
- `vgm_source_database/templates/base.html`
  - Removed Bootstrap 5 CSS and JavaScript CDN links
  - Added Tailwind CSS (compiled from input.css)
  - Added Alpine.js with collapse plugin
  - Converted navbar from Bootstrap to Tailwind with retro neon styling
  - Converted alerts to use Alpine.js for dismiss functionality
  - Updated layout to use Tailwind utility classes
- `.cursor/rules/general/button-styling.mdc`
  - Updated to reference Tailwind CSS classes instead of Bootstrap
  - Maintained backward compatibility with existing class names (btn-success, btn-primary, btn-info, btn-danger)
  - Added documentation about neon color mapping

**Key Features:**
- Dark theme with custom dark color palette (dark-bg, dark-surface, dark-card, dark-border)
- Retro neon color palette (cyan, pink, green, yellow, orange, purple, blue)
- Custom neon glow effects for buttons, shadows, and text
- Backward-compatible button classes that map to neon colors
- Responsive navigation with Alpine.js mobile menu
- Custom form styling with neon focus states
- Monospace font family for retro aesthetic

**Build Instructions:**
- Run `npm install` to install dependencies
- Run `npm run build:css` to compile Tailwind CSS
- For development, use `npm run watch:css` to automatically rebuild CSS on changes

## 2024-12-19

### Updated Cursor Rules: HTMX → Alpine.js + TailwindCSS

**Changed Files:**
- `.cursor/rules/general/django-best-practices.mdc`
  - Replaced HTMX attributes (`hx-get`, `hx-target`, etc.) with Alpine.js directives (`x-data`, `x-show`, `@click`, etc.)
  - Updated to emphasize TailwindCSS utility classes over custom CSS
  - Removed HTMX-specific navigation patterns

- `.cursor/rules/general/django-class-based-views.mdc`
  - Removed HTMX-specific checks (`self.request.htmx`)
  - Updated to use standard Django redirect patterns instead of HTMX responses
  - Removed partial template requirements

- `.cursor/rules/general/django-detail-views.mdc`
  - Replaced HTMX attributes with standard Django links and Alpine.js for interactivity
  - Updated examples to use TailwindCSS classes instead of Bootstrap
  - Changed template pattern to extend base.html instead of being partials

- `.cursor/rules/general/django-modal-forms.mdc`
  - Updated to use Alpine.js `x-show`/`x-if` for modal visibility
  - Changed from HTMX form submission to standard Django forms or Alpine.js AJAX
  - Updated styling references from Bootstrap to TailwindCSS

- `.cursor/rules/general/python-django-general.mdc`
  - Changed dependencies from "Htmx" and "Bootstrap 5" to "Alpine.js" and "TailwindCSS"
  - Updated expert description to include Alpine.js and TailwindCSS
  - Updated guidance to prefer Alpine.js over vanilla JavaScript

- `.cursor/rules/general/django-form-handling.mdc`
  - Removed HTMX-specific reference
  - Updated to mention Alpine.js AJAX as an option

- `.cursor/rules/general/django-htmx-view-context.mdc`
  - Marked as deprecated with note that it's not applicable to Alpine.js stack
  - Alpine.js doesn't use the same partial loading patterns as HTMX

**Summary:**
All Cursor rules have been updated to reflect the new tech stack: Django + Alpine.js + TailwindCSS, replacing the previous HTMX + Bootstrap 5 stack. Rules now focus on Alpine.js directives for interactivity and TailwindCSS utility classes for styling.

## 2024-12-19 - Created VGM Database Models Structure

**Created Files:**

### Sources App (`vgm_source_database/sources/`)
- `__init__.py` - App initialization
- `apps.py` - App configuration (SourcesConfig)
- `models.py` - Models: Company, Product, Bank, SoundSource
- `admin.py` - Admin interfaces for all models
- `migrations/__init__.py` - Migrations directory

**Key Features:**
- `Company` model with unique name
- `Product` model with unique_together constraint on (name, company)
- `Bank` model with unique_together constraint on (name, product)
- `SoundSource` model with custom validation ensuring either bank OR product is set (not both, not neither)
- ManyToMany relationships to User (discoverers), Game, and Song

### Games App (`vgm_source_database/games/`)
- `__init__.py` - App initialization
- `apps.py` - App configuration (GamesConfig)
- `models.py` - Models: GameTag, Game
- `admin.py` - Admin interfaces for all models
- `migrations/__init__.py` - Migrations directory

**Key Features:**
- `GameTag` model with auto-generated slug from name
- `Game` model with release_date, release_year, album_artists (ManyToMany to Person), and tags

### Songs App (`vgm_source_database/songs/`)
- `__init__.py` - App initialization
- `apps.py` - App configuration (SongsConfig)
- `models.py` - Models: Person, Song
- `admin.py` - Admin interfaces for all models
- `migrations/__init__.py` - Migrations directory

**Key Features:**
- `Person` model with ManyToMany to Product (for tracking preferred gear)
- `Song` model with ForeignKey to Game, ManyToMany to Person (composers and arrangers), and track_number
- unique_together constraint on (title, game) for songs

**Modified Files:**
- `config/settings/base.py`
  - Added `vgm_source_database.sources` to LOCAL_APPS
  - Added `vgm_source_database.games` to LOCAL_APPS
  - Added `vgm_source_database.songs` to LOCAL_APPS

**Model Relationships Implemented:**
- Company → Product (one-to-many)
- Product → Bank (one-to-many, optional)
- Product → SoundSource (one-to-many, if no bank)
- Bank → SoundSource (one-to-many)
- Game → Song (one-to-many)
- Game → GameTag (many-to-many)
- Song → Person (many-to-many, for composers and arrangers)
- Game → Person (many-to-many, for album_artists/sound teams)
- Person → Product (many-to-many, for tracking preferred gear)
- SoundSource → Game (many-to-many, soundtrack-level)
- SoundSource → Song (many-to-many, song-level)
- SoundSource → User (many-to-many, for discoverers/credits)

**Next Steps:**
- Run `python manage.py makemigrations sources games songs` to create initial migrations
- Run `python manage.py migrate` to apply migrations to the database

## 2024-12-19 - Added Views, URLs, and Dashboard

**Created Files:**

### Views
- `vgm_source_database/views.py` - Dashboard HomeView with stats and recent activity
- `vgm_source_database/sources/views.py` - Views for Company, Product, Bank, SoundSource
- `vgm_source_database/games/views.py` - Views for Game and GameTag
- `vgm_source_database/songs/views.py` - Views for Song and Person

### URL Configuration
- `vgm_source_database/sources/urls.py` - URL patterns for sources app
- `vgm_source_database/games/urls.py` - URL patterns for games app
- `vgm_source_database/songs/urls.py` - URL patterns for songs app

### Templates
- `templates/pages/home.html` - Dashboard homepage with stats, quick actions, and recent activity
- `templates/sources/` - 12 templates (list, detail, form for each model)
- `templates/games/` - 6 templates (list, detail, form for each model)
- `templates/songs/` - 6 templates (list, detail, form for each model)

**Modified Files:**
- `config/urls.py`
  - Changed homepage from TemplateView to HomeView
  - Added URL includes for sources, games, and songs apps
- `templates/base.html`
  - Added navbar links to Sources, Games, and Songs

**Features Implemented:**
- Dashboard with statistics cards for all major object types
- Quick Actions section with create buttons (requires authentication)
- Recent Activity widget showing last 10 items created
- Complete CRUD views for all models (List, Detail, Create)
- Proper button styling following project rules (btn-success for create, btn-primary for view)
- All templates use Bootstrap 5 styling
- URL namespacing for all apps (sources, games, songs)

## 2024-12-19 - Added Complete CRUD Views and Dashboard Enhancements

**Modified Files:**

### Views
- `vgm_source_database/sources/views.py`
  - Added UpdateView and DeleteView for Company, Product, Bank, SoundSource
  - All views use LoginRequiredMixin for authentication
- `vgm_source_database/games/views.py`
  - Added UpdateView and DeleteView for Game and GameTag
  - GameTag views use slug_url_kwarg for slug-based routing
- `vgm_source_database/songs/views.py`
  - Added UpdateView and DeleteView for Song and Person

### URL Configuration
- `vgm_source_database/sources/urls.py`
  - Added URL patterns for update and delete views (companies, products, banks, soundsources)
- `vgm_source_database/games/urls.py`
  - Added URL patterns for update and delete views (games, gametags)
- `vgm_source_database/songs/urls.py`
  - Added URL patterns for update and delete views (songs, people)

### Templates
- `templates/pages/home.html`
  - Added "Create <object>" buttons next to each "View All" button in statistics cards
  - Buttons only visible for authenticated users
  - Uses flex layout for side-by-side button placement

**Updated List View Templates:**
- `templates/sources/company_list.html` - Added "Back to homepage" link
- `templates/sources/product_list.html` - Added "Back to homepage" link
- `templates/sources/bank_list.html` - Added "Back to homepage" link
- `templates/sources/soundsource_list.html` - Added "Back to homepage" link
- `templates/games/game_list.html` - Added "Back to homepage" link
- `templates/games/gametag_list.html` - Added "Back to homepage" link
- `templates/songs/song_list.html` - Added "Back to homepage" link
- `templates/songs/person_list.html` - Added "Back to homepage" link

**Updated Form Templates:**
- All 8 form templates updated to handle both create and update modes
- Dynamic titles: `{% if object.pk %}Update{% else %}Create{% endif %}`
- Dynamic button classes: `btn-info` for update, `btn-success` for create
- Dynamic button text based on mode

**Created Delete Confirmation Templates:**
- `templates/sources/company_confirm_delete.html`
- `templates/sources/product_confirm_delete.html`
- `templates/sources/bank_confirm_delete.html`
- `templates/sources/soundsource_confirm_delete.html`
- `templates/games/game_confirm_delete.html`
- `templates/games/gametag_confirm_delete.html`
- `templates/songs/person_confirm_delete.html`
- `templates/songs/song_confirm_delete.html`

**Key Features:**
- Complete CRUD operations for all 8 model types
- Authentication required for create, update, and delete operations
- Consistent URL patterns: `<model>/<pk>/update/` and `<model>/<pk>/delete/`
- Dashboard enhancements with quick create buttons
- Navigation improvements with homepage links on all list views
- Form templates support both create and update modes dynamically
- Delete confirmations with proper warnings and cancel options

## 2024-12-19 - Removed Email Requirement for User Registration

**Modified Files:**
- `config/settings/base.py`
  - Removed `"email*"` from `ACCOUNT_SIGNUP_FIELDS` (changed to `["username*", "password1*", "password2*"]`)
  - Changed `ACCOUNT_EMAIL_VERIFICATION` from `"mandatory"` to `"none"`

- `vgm_source_database/users/models.py`
  - Added explicit `email` field override with `blank=True` to ensure email is optional
  - Added import for `EmailField` from `django.db.models`

**Key Changes:**
- Email is no longer required when creating new user accounts
- Users can sign up with only username and password
- Email verification is disabled since email is not mandatory
- Database schema already supported blank emails (from initial migration), so no new migration needed
- Existing users with emails are unaffected

## 2024-12-19 - Enhanced Recent Activity Section to Show All CRUD Actions

**Modified Files:**
- `vgm_source_database/views.py`
  - Added imports for Bank, GameTag models (previously missing)
  - Added import for `F` from `django.db.models` for database-level filtering
  - Refactored recent activity logic to track both creates and updates
  - Created `add_activity_items()` helper function to process querysets
  - Tracks creates using `created_at` timestamp
  - Tracks updates using `updated_at` timestamp (filtered to only include items where `updated_at > created_at`)
  - Includes all 8 model types: Company, Product, Bank, SoundSource, Game, GameTag, Song, Person
  - Changed limit from 10 to 15 operations
  - Activity items now include: action ("Created"/"Updated"), type, name, url, timestamp

- `vgm_source_database/templates/pages/home.html`
  - Updated Recent Activity section to display action type badges
  - "Created" actions use neon-green border and text (`border-neon-green text-neon-green`)
  - "Updated" actions use neon-cyan border and text (`border-neon-cyan text-neon-cyan`)
  - Changed timestamp field from `item.created_at` to `item.timestamp`
  - Action badge displayed alongside model type badge
  - All activity items remain clickable links to detail pages

**Key Features:**
- Tracks both Create and Update operations across all models
- All creates and updates are clickable links to detail pages
- Color-coded action badges for easy visual distinction (green for creates, cyan for updates)
- Limited to the last 15 operations sorted by timestamp (most recent first)
- Comprehensive coverage of all 8 model types in the database

**Technical Details:**
- Uses Django's `F()` expression to filter updates where `updated_at > created_at` at the database level
- Helper function `add_activity_items()` accepts queryset, model name, and functions for getting display name and URL
- Combines all activities into a single list, sorts by timestamp, and limits to 15 most recent

**Note:** Delete operations are not tracked since Django removes deleted objects from the database. To track deletes, an audit log system would need to be implemented.

## 2024-12-19 - Updated Theme from Neon Retro to Modern Dark Theme

**Modified Files:**

### Tailwind Configuration
- `tailwind.config.js`
  - Removed all neon color definitions (neon-cyan, neon-pink, neon-green, etc.)
  - Removed neon glow shadows and animations
  - Updated dark theme colors to modern grays:
    - `dark.bg`: `#111827` (gray-900)
    - `dark.surface`: `#1f2937` (gray-800)
    - `dark.card`: `#374151` (gray-700)
    - `dark.border`: `#4b5563` (gray-600)
  - Added modern accent colors:
    - `accent.primary`: `#3b82f6` (blue-500)
    - `accent.success`: `#10b981` (emerald-500)
    - `accent.info`: `#06b6d4` (cyan-500)
    - `accent.danger`: `#ef4444` (red-500)
    - `accent.warning`: `#f59e0b` (amber-500)
  - Replaced neon shadows with subtle modern shadows (soft, medium, large)

### CSS Styling
- `vgm_source_database/static/css/input.css`
  - Updated body background to `#111827`
  - Replaced all neon button classes with modern solid buttons:
    - `btn-success`: emerald-600 background, white text, rounded corners
    - `btn-primary`: blue-600 background, white text, rounded corners
    - `btn-info`: cyan-600 background, white text, rounded corners
    - `btn-danger`: red-600 background, white text, rounded corners
  - Removed monospace fonts and uppercase styling
  - Updated cards to use subtle borders (`border border-[#4b5563]`)
  - Modernized alerts with subtle borders and muted colors
  - Updated navigation links to use modern hover states
  - Updated form inputs with modern focus states (blue-500)
  - Removed all text glow utilities

### Base Template
- `vgm_source_database/templates/base.html`
  - Updated `@theme` variables to modern dark theme colors
  - Removed all neon color utility classes (text-neon-*, border-neon-*, etc.)
  - Removed neon shadow utilities
  - Updated button components:
    - Solid backgrounds instead of transparent with borders
    - Modern rounded corners and subtle shadows
    - Smooth hover transitions
  - Updated navigation bar:
    - Removed neon cyan borders and shadows
    - Logo uses `text-blue-400` instead of neon cyan
    - Removed monospace and uppercase styling
    - Modern border styling (`border-b border-[#4b5563]`)
  - Updated alerts to use modern styling with subtle borders
  - Removed all text glow utilities
  - Updated mobile menu button to use modern colors

### Documentation
- `.cursor/rules/general/button-styling.mdc`
  - Updated description from "retro neon theme" to "modern dark theme"
  - Changed color references from neon colors to modern Tailwind colors
  - Removed references to glow effects
  - Updated button descriptions to reflect solid backgrounds

**Key Changes:**
- Theme migrated from bright neon retro aesthetic to modern, professional dark theme
- All buttons now use solid backgrounds with subtle hover effects
- Removed all glowing effects and animations
- Typography changed from monospace/uppercase to modern sans-serif
- Color palette uses muted, professional colors instead of bright neon
- Shadows and borders are subtle instead of glowing
- Better readability and less eye strain
- Consistent with contemporary dark theme design patterns (inspired by syntax.tailwindui.com)

**Color Scheme:**
- Background: `#111827` (gray-900)
- Surfaces: `#1f2937` (gray-800), `#374151` (gray-700)
- Borders: `#4b5563` (gray-600)
- Accents: Blue (`#3b82f6`), Emerald (`#10b981`), Cyan (`#06b6d4`), Red (`#ef4444`)
- Text: Light gray with blue accents on hover

## 2024-12-19 - Fixed Form Styling for Dark Theme

**Modified Files:**
- `vgm_source_database/templates/base.html`
  - Added comprehensive CSS styling for all Bootstrap5 form elements to work with dark theme
  - Fixed dropdown/select elements that showed white text on white background
  - All form controls now have dark backgrounds (#374151) with light text (#f3f4f6)

**Key Changes:**
- Styled `.form-control`, `.form-select`, and `select` elements:
  - Dark background (#374151) with light text (#f3f4f6)
  - Dark border (#4b5563) with blue focus state (#3b82f6)
  - Proper focus box-shadow for visual feedback
- Styled select dropdown options:
  - Dark background (#374151) with light text (#f3f4f6)
  - Ensures dropdown options are visible
- Form labels:
  - Light gray text (#d1d5db) with proper font weight
  - Required field indicators with red asterisk
- Form help text and error messages:
  - Help text uses muted gray (#9ca3af)
  - Error messages use red accent (#f87171)
  - Success states use green accent (#10b981)
- Checkboxes and radio buttons:
  - Dark backgrounds with blue accent when checked
  - Proper focus states
- Disabled and readonly controls:
  - Darker background (#1f2937) with reduced opacity
  - Muted text color (#6b7280)
- Input groups and form rows:
  - Proper spacing and alignment
  - Dark theme compatible styling

**Form Elements Styled:**
- Text inputs (`.form-control`)
- Select dropdowns (`.form-select`, `select.form-control`)
- Textareas (`textarea.form-control`)
- Checkboxes (`.form-check-input`)
- Radio buttons (`.form-check-input[type="radio"]`)
- Form labels (`.form-label`, `label`)
- Help text (`.form-text`, `.help-block`, `.help-text`)
- Error messages (`.invalid-feedback`, `.errorlist`)
- Validation states (`.is-invalid`, `.is-valid`)
- Input groups (`.input-group-text`)
- Disabled/readonly states

**Result:**
- All form elements now have consistent dark theme styling
- Dropdowns are fully visible with dark backgrounds and light text
- Improved readability and visual consistency across all forms
- Proper focus states and validation feedback
- Better user experience with clear visual hierarchy

## 2024-12-19 - Updated Form Field Backgrounds for Better Contrast

**Modified Files:**
- `vgm_source_database/templates/base.html`
  - Changed form field backgrounds from `#374151` (card background) to `#111827` (main background)
  - Updated all form control types: inputs, selects, textareas, checkboxes, radio buttons
  - Updated focus states to maintain darker background
  - Updated validation states (is-invalid, is-valid) to use darker background
  - Updated select dropdown options to use darker background
  - Updated disabled/readonly controls to use even darker shade (#0f1419)

**Key Changes:**
- Form controls now use `#111827` (gray-900) instead of `#374151` (gray-700)
- Creates visual contrast between form fields and the card container
- Disabled controls use `#0f1419` (darker than main background) for better distinction
- All states (normal, focus, valid, invalid) maintain consistent darker background

**Result:**
- Better visual hierarchy with form fields standing out against card background
- Improved contrast makes input areas easier to identify
- Maintains readability with light text (#f3f4f6) on dark background
- Consistent styling across all form element types

## 2024-12-19 - Added CSV to YAML Conversion Script

**Created Files:**
- `convert_csv_to_yaml.py` - CSV conversion script
  - Processes CSV files matching `NEWER VGM Sound Sources - *.csv`
  - Extracts GameTag names from filenames
  - Detects game title rows and groups sound sources between them
  - Handles release dates in Product column
  - Generates YAML fixtures in dependency order
  - Creates skipped lines report

**Key Features:**
- Game title detection from "Company/Manufacturer" column
- Sound source parsing from "Program" column
- Relationship resolution for Companies, Products, Banks, Games
- Smart skipping of section headers and invalid rows

## 2024-12-19 - Added Import Data Functionality to GUI

**Created Files:**
- `vgm_source_database/forms.py` - Import form with file upload
  - `ImportDataForm` with YAML file upload field
  - Dry-run checkbox for validation
- `vgm_source_database/urls.py` - URL routing for data management
  - Import route at `/import/` with namespace `data`
- `vgm_source_database/templates/pages/import_data.html` - Import page template
  - File upload form with instructions
  - Dry-run validation option
  - Success/error message display

**Modified Files:**
- `vgm_source_database/views.py` - Added `ImportDataView`
  - FormView for handling file uploads
  - Requires authentication (LoginRequiredMixin)
  - Supports dry-run validation
  - Performs actual import using `loaddata` command
  - Shows success/error messages
- `vgm_source_database/templates/base.html` - Added Data Management section
  - New section below "Top Categories" in sidebar
  - "Import YAML" button (authenticated users only)
  - Consistent styling with existing sidebar
- `config/urls.py` - Added import URL routing

**Key Features:**
- File upload through web interface
- Dry-run validation before import
- Authentication required
- Clear error messages
- Consistent dark theme styling

## 2024-12-19 - Fixed Fixture Import Error: Model Reference Format

**Problem:**
Import was failing with "too many values to unpack (expected 2)" error. The dry-run validation passed, but actual import failed because Django's fixture loader expects model references in format `app_label.ModelName` (2 parts), but the converter was generating `vgm_source_database.app.ModelName` (3 parts).

**Solution:**
1. Fixed model reference format in `convert_csv_to_yaml.py`:
   - All model references changed from `vgm_source_database.app.Model` to `app.Model`
   - Updated 6 model references: GameTag, Game, Company, Product, Bank, SoundSource

2. Enhanced dry-run validation in `ImportDataView`:
   - Now validates Django fixture format, not just YAML syntax
   - Checks for required keys (`model`, `pk`, `fields`)
   - Validates model format (exactly 2 parts: `app_label.ModelName`)
   - Validates `fields` is a dictionary
   - Provides specific error messages with item index

**Files Modified:**
- `convert_csv_to_yaml.py` - Fixed model reference formats
- `vgm_source_database/views.py` - Enhanced dry-run validation

**Impact:**
- Newly generated fixtures will use correct format and import successfully
- Existing fixtures with wrong format need to be regenerated
- Dry-run now catches format errors before attempting import

## 2024-12-19 - Fixed Missing created_at and updated_at Fields in Fixtures

**Problem:**
Import was failing with "null value in column 'created_at' violates not-null constraint". Django's `loaddata` doesn't auto-populate `auto_now_add`/`auto_now` fields when missing from fixtures.

**Solution:**
1. Added `datetime` and `timezone` imports to converter
2. Added `created_at` and `updated_at` fields to all model fixtures:
   - GameTag, Game, Company, Product, Bank, SoundSource
3. Used UTC timezone-aware datetime in ISO format

**Files Modified:**
- `convert_csv_to_yaml.py` - Added timestamp fields to all fixture generation

**Impact:**
- All generated fixtures now include required timestamp fields
- Import works without constraint violations
- Timestamps use proper ISO format with UTC timezone

## 2024-12-19 - Fixed Unicode Characters in GameTag Slugs

**Problem:**
Import failed with URL reverse error because slug "pokémon" contains Unicode character (é) that doesn't match URL pattern `[-a-zA-Z0-9_]+`.

**Solution:**
1. Added `unicodedata` import for Unicode normalization
2. Enhanced `slugify()` method to:
   - Normalize Unicode to ASCII (NFKD normalization)
   - Remove diacritics (é → e, ñ → n)
   - Ensure only ASCII alphanumeric, underscore, hyphen characters

**Files Modified:**
- `convert_csv_to_yaml.py` - Enhanced slugify with Unicode normalization

**Impact:**
- Unicode characters converted to ASCII in slugs
- "pokémon" → "pokemon" (matches URL pattern)
- Slugs work with Django URL routing

**Created Files:**
- `config/management/commands/fix_gametag_slugs.py` - Management command to fix existing slugs
- `fix_slugs_now.py` - Quick fix script for immediate use

**Usage:**
- Quick fix: `python fix_slugs_now.py`
- Management command: `python manage.py fix_gametag_slugs [--dry-run]`

## 2024-12-19 - Fixed Missing Fallback Products in Fixtures

**Problem:**
Sources import failed with foreign key constraint violation. SoundSource referenced Product pk=1719 that didn't exist because fallback products were created after products_yaml generation.

**Solution:**
1. Moved fallback product creation from `generate_yaml()` to `resolve_relationships()`
2. Fallback products now created before products_yaml generation
3. All products (including fallbacks) included in YAML fixture

**Files Modified:**
- `convert_csv_to_yaml.py` - Moved fallback product creation earlier in process

**Impact:**
- All fallback products included in fixtures
- Foreign key constraints satisfied
- SoundSources can reference fallback products that exist

## 2024-12-19 - Added Combined Fixture File Option

**Feature:**
Added support for generating a single combined fixture file containing all models in dependency order.

**Solution:**
1. Added `combined_file` parameter to CSVConverter
2. Modified generate_yaml() to combine all fixtures when enabled
3. Added `--combined` command-line argument
4. Combined file named `all_fixtures.yaml` with all models in order

**Usage:**
```bash
python convert_csv_to_yaml.py --combined
```

**Files Modified:**
- `convert_csv_to_yaml.py` - Added combined file support

**Impact:**
- Single file import instead of multiple files
- All models in correct dependency order
- Simplified import process

## 2024-12-19 - Added Duplicate Handling to Importer

**Feature:**
Added duplicate handling options to prevent import failures when duplicates are encountered.

**Solution:**
1. Created custom import function in `import_utils.py`
2. Added duplicate_handling option to form and command
3. Supports "skip" (default) and "overwrite" modes
4. Properly handles ManyToMany and ForeignKey relationships
5. Provides detailed import statistics

**Files Created:**
- `vgm_source_database/import_utils.py` - Custom import with duplicate handling

**Files Modified:**
- `vgm_source_database/forms.py` - Added duplicate_handling field
- `vgm_source_database/views.py` - Uses custom import function
- `config/management/commands/import_data.py` - Added --duplicate-handling option

**Usage:**
```bash
# Skip duplicates (default)
python manage.py import_data --file fixtures/all_fixtures.yaml

# Overwrite duplicates
python manage.py import_data --file fixtures/all_fixtures.yaml --duplicate-handling overwrite
```

**Impact:**
- Imports no longer fail on duplicates
- Users can choose skip or overwrite behavior
- Detailed statistics provided
- Better error handling

