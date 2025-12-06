# Chat History

## 2024-12-19 - Created Unified Import/Export System for YAML Fixtures

### User Request
We need to be able to import/export data from this app. Imports and exports should be via fixtures in yaml. Go through the existing models and write out rules and documentation for doing this, along with examples for each type. This should be using one unified import/export mechanism.

### Response
Created a comprehensive unified import/export system for the VGM Source Database using YAML fixtures. The system includes management commands, detailed documentation, and examples for all model types.

**Solution:**
- Created management commands for export (`export_data`) and import (`import_data`)
- Created comprehensive documentation guide (`ai_docs/IMPORT_EXPORT_GUIDE.md`)
- Created example fixture files for all model types
- Updated import-file-creation rule to be specific to this project
- Created fixtures directory structure with README

**Key Features:**
- **Export Command**: `python manage.py export_data` - exports all data to YAML fixtures
  - Supports filtering by app (`--app games`)
  - Supports custom output directory (`--output-dir`)
  - Supports JSON format (`--format json`)
- **Import Command**: `python manage.py import_data` - imports data from YAML fixtures
  - Supports dry-run mode for validation (`--dry-run`)
  - Supports single file import (`--file`)
  - Automatically handles dependency ordering
- **Documentation**: Comprehensive guide covering:
  - All model types with field specifications
  - Field value handling rules (null vs empty string)
  - Relationship handling (ForeignKey, ManyToMany)
  - Best practices and troubleshooting
- **Examples**: Complete example fixtures for all 8 model types:
  - GameTag, Game, Person, Song
  - Company, Product, Bank, SoundSource

**Files Created:**
- `config/management/commands/export_data.py` - Export management command
- `config/management/commands/import_data.py` - Import management command
- `ai_docs/IMPORT_EXPORT_GUIDE.md` - Comprehensive documentation
- `fixtures/README.md` - Fixtures directory documentation
- `fixtures/examples/` - Example fixture files for all models

**Files Modified:**
- `.cursor/rules/general/import-file-creation.mdc` - Updated with VGM-specific examples

**Result:**
- Unified import/export system using Django's fixture mechanism
- Human-readable YAML format for version control
- Automatic dependency handling and ordering
- Comprehensive documentation with examples for each model type
- Easy-to-use management commands for data migration

## 2024-12-19 - Updated Navbar App Name

### User Request
Also on the dashboard, the navbar refers to our app as the "VGM Source Database" - let's be even more explicit and make this "The VGM Sound Source Database"

### Response
Updated the navbar app name to be more explicit about the purpose of the database.

**Solution:**
- Updated `vgm_source_database/templates/base.html`
- Changed navbar link text from "VGM Source Database" to "The VGM Sound Source Database"
- Also updated the default page title to match for consistency

**Result:**
- Navbar now displays "The VGM Sound Source Database" as the app name
- Page title also updated for consistency across all pages
- More explicit naming clarifies the database's focus on sound sources

## 2024-12-19 - Reordered Dashboard Statistics Blocks

### User Request
On the dashboard, let's re-order the Statistics blocks. From left to right across the top, we want Sound Sources, Games, Songs. In the second row, we want Products, Companies, People

### Response
Reordered the statistics blocks on the dashboard to match the requested layout.

**Solution:**
- Updated `vgm_source_database/templates/pages/home.html`
- Reordered the statistics cards within the grid layout
- First row (left to right): Sound Sources, Games, Songs
- Second row (left to right): Products, Companies, People

**Result:**
- Statistics blocks now display in the requested order
- Grid layout (3 columns on large screens) automatically wraps to create two rows
- All functionality and styling remain unchanged

## 2024-12-19 - Fixed GameTag URL Pattern Ordering

### User Request
Clicking on Create Tag leads to a 404 error: "No Game Tag found matching the query". The URL `games/tags/create/` is being matched by the `gametag_detail` pattern instead of `gametag_create`.

### Response
Fixed the URL pattern ordering issue in `vgm_source_database/games/urls.py`. The problem was that the more general pattern `tags/<slug:slug>/` was placed before the more specific pattern `tags/create/`, causing Django to match "create" as a slug parameter.

**Solution:**
- Reordered URL patterns so `tags/create/` comes before `tags/<slug:slug>/`
- This follows Django best practice: more specific patterns should come before general patterns
- Django matches URL patterns in order, so the first matching pattern is used

**Technical Details:**
- Moved `path("tags/create/", GameTagCreateView.as_view(), name="gametag_create")` before `path("tags/<slug:slug>/", GameTagDetailView.as_view(), name="gametag_detail")`
- Now when Django processes `games/tags/create/`, it matches the create pattern first instead of trying to find a tag with slug="create"

**Result:**
- Tag creation URL now works correctly
- No more 404 errors when clicking "Create Tag" button

## 2024-12-19 - Added Tag CRUD Views, Dashboard Button, and Sidebar with Top Categories

### User Request
Let's add crud views, and to the dashboard add a "Create Tag" button.

In addition, let's add a sidebar now that sites outside the main content window, similar to the navbar. For now, just add a list of Tags, sorted by most occurrences. We can call this section "Top Categories"

### Response
Added the "Create Tag" button to the dashboard and implemented a sidebar with the Top Categories section showing tags sorted by occurrence count.

**Solution:**

1. **Added "Create Tag" Button to Dashboard:**
   - Updated `vgm_source_database/templates/pages/home.html`
   - Added "Create Tag" button to the Quick Actions section
   - Button uses `btn-success` class and links to `games:gametag_create`
   - Only visible to authenticated users (consistent with other create buttons)

2. **Created Context Processor for Top Tags:**
   - Created `vgm_source_database/games/context_processors.py`
   - Implemented `top_categories()` function that:
     - Uses Django's `Count` aggregation to count games per tag
     - Filters tags with at least one game (`game_count__gt=0`)
     - Orders by game count descending
     - Limits to top 20 tags for performance
   - Added context processor to `config/settings/base.py` TEMPLATES configuration
   - Makes `top_categories` available in all templates automatically

3. **Added Sidebar to Base Template:**
   - Updated `vgm_source_database/templates/base.html`
   - Restructured layout to use flexbox with sidebar on left and main content on right
   - Sidebar features:
     - Fixed width (w-64) with dark theme styling
     - Sticky positioning (stays visible when scrolling)
     - "Top Categories" heading with neon-cyan styling
     - List of tags with:
       - Tag name as clickable link to tag detail page
       - Game count in parentheses showing occurrence
       - Hover effects matching site theme
     - Empty state message when no tags exist
   - Main content area adjusted to work alongside sidebar

**Key Features:**
- CRUD views for GameTag already existed, so no changes needed to views/URLs
- Quick access to tag creation from dashboard
- Sidebar provides easy navigation to popular tags
- Visual indication of tag popularity through occurrence counts
- Sidebar sits outside main content window (similar to navbar positioning)
- Consistent dark theme styling throughout
- Efficient database queries using Django ORM aggregation

**Technical Details:**
- Uses `GameTag.objects.annotate(game_count=Count("games"))` for efficient counting
- Context processor pattern ensures top categories are available site-wide
- Flexbox layout ensures sidebar and main content work together responsively
- Sticky positioning keeps sidebar visible during scrolling
- Tags are sorted by most occurrences (highest game_count first)

## 2024-12-19 - Converted Games Detail Page Songs List to Table with Sources

### User Request
When we go to the Games detail page for a particular game, we see the release year and then a Songs list. Let's make this a table with each song in the first column, and then a list of the sources for that game in the second column. Each song and source should be able to be clicked to navigate to that object's detail page.

### Response
Converted the songs list on the Games detail page to a table format showing songs and their associated sound sources.

**Solution:**
1. **Updated GameDetailView (`vgm_source_database/games/views.py`):**
   - Added `get_queryset()` method to optimize database queries
   - Used `prefetch_related()` to load songs and their sound sources efficiently
   - Prevents N+1 query issues when accessing sound sources for each song
   - Also prefetches tags and album_artists for better performance

2. **Updated Template (`vgm_source_database/templates/games/game_detail.html`):**
   - Replaced the vertical list of songs with a table layout
   - First column: Song names (with track numbers if available) as clickable links to song detail pages
   - Second column: Sound sources for each song displayed as comma-separated clickable links to source detail pages
   - Empty state shows "-" when a song has no associated sources
   - Table styling matches other list views in the project (consistent with song_list.html)

**Key Features:**
- Table format provides better organization and readability
- Both songs and sources are clickable links for easy navigation
- Optimized database queries prevent performance issues
- Consistent styling with other table views in the application
- Handles empty states gracefully (songs without sources show "-")

**Technical Details:**
- Uses `prefetch_related("songs__sound_sources")` to load all related data in efficient queries
- Table structure follows the same pattern as other list views in the project
- Links use the same URL patterns and styling as elsewhere in the application

## 2024-12-19 - Fixed Recent History Duplicate Entries on Object Creation

### User Request
The Recent History shows two entries when an object is created - one for the created and an "updated" entry as well. When an object is created we do not need to see an updated entry.

### Response
Fixed the issue where newly created objects appeared twice in Recent History (once as "Created" and once as "Updated"). 

**Solution:**
- Modified `vgm_source_database/views.py` to track objects that have been added as "Created" using a set of URLs
- When processing "Updated" entries, the code now skips any object whose URL is already in the `created_urls` set
- This ensures that newly created objects only appear once as "Created" and won't also appear as "Updated"

**Technical Details:**
- Added `created_urls = set()` to track URLs of objects added as "Created"
- Modified `add_activity_items()` helper function to:
  1. Add each object's URL to `created_urls` when adding it as "Created"
  2. Check if an object's URL is in `created_urls` before adding it as "Updated"
- This prevents duplicate entries while still showing legitimate updates for objects that were created earlier

## 2024-12-19 - Updated Cursor Rules from HTMX to Alpine.js

### User Request
In the .cursor directory, I have added a bunch of rules for this new project. Please review all instances of "HTMX" and change/update these rules for Alpine.js instead. Our stack for this project will be django with tailwindcss and alpine.js, instead of HTMX. If the rule is not relevant to tailwindcss or alpine, remove it.

### Response
Updated all Cursor rules in the `.cursor/rules/general/` directory to replace HTMX references with Alpine.js patterns. The following files were updated:

1. **django-best-practices.mdc** - Updated to focus on Alpine.js directives and TailwindCSS utility classes instead of HTMX attributes
2. **django-class-based-views.mdc** - Removed HTMX-specific patterns like `self.request.htmx` checks
3. **django-detail-views.mdc** - Updated to use Alpine.js patterns and TailwindCSS styling instead of HTMX attributes
4. **django-modal-forms.mdc** - Updated to use Alpine.js for modal handling instead of HTMX
5. **python-django-general.mdc** - Updated dependencies to reference Alpine.js and TailwindCSS instead of HTMX and Bootstrap 5
6. **django-form-handling.mdc** - Removed HTMX-specific reference
7. **django-htmx-view-context.mdc** - Marked as deprecated since it's not applicable to Alpine.js stack

All rules now focus on:
- Alpine.js for client-side interactivity (using `x-data`, `x-show`, `@click`, etc.)
- TailwindCSS utility classes for styling
- Standard Django patterns for server-side handling

## 2024-12-19 - Created VGM Database Models Structure

### User Request
Please follow the plan and build out the components listed for our app.

### Response
Created three Django apps with all models, admin interfaces, and migrations structure as specified in the plan:

1. **sources app** - Created with models:
   - `Company` - Companies that produce sound products
   - `Product` - Products (hardware/software) produced by companies
   - `Bank` - Banks within products
   - `SoundSource` - Sound sources (samples, patches) with validation to ensure either bank OR product is set

2. **games app** - Created with models:
   - `GameTag` - Tags for categorizing games (with auto-generated slugs)
   - `Game` - Video games with release dates/years, album artists, and tags

3. **songs app** - Created with models:
   - `Person` - People (composers, arrangers, sound team members) with preferred products
   - `Song` - Songs from games with composers, arrangers, and track numbers

All models include:
- Proper relationships (ForeignKeys, ManyToManyFields)
- `created_at` and `updated_at` timestamps
- `notes` fields for additional information
- `__str__` methods for admin display
- `get_absolute_url` methods for URL routing
- Comprehensive admin interfaces with list displays, filters, and search

Updated `config/settings/base.py` to add all three apps to `LOCAL_APPS`.

**Next Steps:**
- Run `python manage.py makemigrations` to create initial migrations
- Run `python manage.py migrate` to apply migrations to the database

## 2024-12-19 - Added Views, URLs, and Dashboard

### User Request
Let's add some views. The homepage should have links in the navbar to Sources, Games, and Products for now. In addition, let's add some buttons for creating/viewing the major objects in the main content window. Let's also add some other common Dashboard widgets, like Recent Activity, and a Stats block showing counts for the various object types.

### Response
Created comprehensive views, URLs, templates, and a dashboard for all three apps:

1. **Views Created:**
   - Sources app: ListView, DetailView, and CreateView for Company, Product, Bank, and SoundSource
   - Games app: ListView, DetailView, and CreateView for Game and GameTag
   - Songs app: ListView, DetailView, and CreateView for Song and Person
   - Dashboard HomeView with stats and recent activity

2. **URL Configuration:**
   - Added URL patterns for all three apps in `config/urls.py`
   - Created `urls.py` files for sources, games, and songs apps with proper namespacing

3. **Navbar Updates:**
   - Added links to Sources, Games, and Songs in the main navigation bar

4. **Dashboard Features:**
   - Statistics cards showing counts for Companies, Products, Sound Sources, Games, Songs, and People
   - Quick Actions section with create buttons for all major objects (requires authentication)
   - Recent Activity widget showing the last 10 items created across all models

5. **Templates Created:**
   - List, detail, and form templates for all models
   - Dashboard homepage template with Bootstrap styling
   - All templates follow Django best practices with proper button styling (btn-success for create, btn-primary for view, etc.)

All views use Django class-based views and follow the project's coding standards. The dashboard provides a comprehensive overview of the database with easy navigation to all major sections.

## 2024-12-19 - Switched Theme to Tailwind CSS with Dark Retro Neon Colors

### User Request
Let's switch our main theme to Tailwindcss. We want a dark theme with retro neon colors

### Response
Successfully migrated the project from Bootstrap 5 to Tailwind CSS with a dark retro neon theme. Here's what was implemented:

1. **Package Configuration:**
   - Created `package.json` with Tailwind CSS, PostCSS, and Autoprefixer dependencies
   - Added build scripts for CSS compilation (`npm run build:css` and `npm run watch:css`)

2. **Tailwind Configuration:**
   - Created `tailwind.config.js` with:
     - Dark mode enabled by default
     - Custom retro neon color palette (cyan, pink, green, yellow, orange, purple, blue)
     - Custom neon glow shadows and animations
     - Dark background colors (dark-bg, dark-surface, dark-card, dark-border)
     - Custom font family for retro aesthetic (Courier New monospace)

3. **PostCSS Configuration:**
   - Created `postcss.config.js` for processing Tailwind CSS

4. **CSS Styling:**
   - Created `vgm_source_database/static/css/input.css` with:
     - Tailwind directives (@tailwind base, components, utilities)
     - Custom component classes for retro neon buttons (btn-neon-cyan, btn-neon-pink, etc.)
     - Backward-compatible button classes (btn-success, btn-primary, btn-info, btn-danger) that map to neon colors
     - Custom alert styles with neon borders
     - Navigation link styles with neon hover effects
     - Form input and label styles with neon focus states
     - Text glow utilities for neon text effects

5. **Template Updates:**
   - Updated `base.html` to:
     - Remove Bootstrap CSS and JavaScript
     - Add Tailwind CSS (compiled from input.css)
     - Add Alpine.js with collapse plugin for mobile navigation
     - Convert navbar to Tailwind with retro neon styling
     - Convert alerts to use Alpine.js for dismiss functionality
     - Update container and layout to use Tailwind utility classes

6. **Rule Updates:**
   - Updated `.cursor/rules/general/button-styling.mdc` to reference Tailwind classes instead of Bootstrap classes
   - Maintained backward compatibility by keeping the same class names (btn-success, btn-primary, etc.) but mapping them to neon colors

**Next Steps:**
- Run `npm install` to install dependencies
- Run `npm run build:css` to compile Tailwind CSS
- For development, use `npm run watch:css` to automatically rebuild CSS on changes
- Existing templates will continue to work with the backward-compatible button classes, but can be gradually updated to use the new Tailwind utility classes directly

## 2024-12-19 - Fixed Tailwind CSS Build Issues

### User Request
Okay, I installed NPM and ran the build and watch commands. When I load my homepage all styling is gone now. Please review the tailwindcss and other settings

### Response
Identified and fixed several issues with the Tailwind CSS configuration:

1. **Fixed CSS compilation issues:**
   - Updated `input.css` to use Tailwind arbitrary values (`[#00ffff]`) instead of custom color names in `@apply` directives
   - This prevents compilation errors when custom colors aren't available during the build process

2. **Fixed dark mode:**
   - Added `class="dark"` to the HTML element in `base.html` to enable dark mode

3. **Updated Tailwind config:**
   - Added additional content paths to ensure all templates are scanned
   - Verified configuration is correct

4. **Simplified base styles:**
   - Changed body styles to use arbitrary values instead of custom color references

**Troubleshooting:**
If the CSS still isn't compiling, check:
- Run `npm run build:css` and look for error messages
- Verify Tailwind is installed: `npm list tailwindcss`
- Check if `project.css` file is created after build
- The build may be failing silently - check for any error output

The CSS should now compile correctly with the arbitrary value syntax.

## 2024-12-19 - Converted All Templates to Tailwind CSS and Alpine.js

### User Request
The file should be here: 'R:\\repos\\vgm_source_database\\vgm_source_database\\static\\css\\input.css'
Make sure the home template (and all templates) use tailwind and alpine instead of bootstrap

### Response
Systematically converted all templates from Bootstrap to Tailwind CSS with Alpine.js:

**Updated Templates:**
1. **Games App:**
   - `game_list.html` - Converted to Tailwind grid and card components
   - `game_detail.html` - Updated with Tailwind styling and neon theme
   - `game_form.html` - Form styling with Tailwind
   - `gametag_list.html`, `gametag_detail.html`, `gametag_form.html` - All converted

2. **Songs App:**
   - `song_list.html`, `song_detail.html`, `song_form.html` - Converted
   - `person_list.html`, `person_detail.html`, `person_form.html` - Converted

3. **Sources App:**
   - `company_list.html`, `company_detail.html`, `company_form.html` - Converted
   - `product_list.html`, `product_detail.html`, `product_form.html` - Converted
   - `bank_list.html`, `bank_detail.html`, `bank_form.html` - Converted
   - `soundsource_list.html`, `soundsource_detail.html`, `soundsource_form.html` - Converted

4. **Users App:**
   - `user_detail.html`, `user_form.html` - Converted

5. **Pages:**
   - `home.html` - Already converted (dashboard with Tailwind)

**Key Changes:**
- Replaced Bootstrap classes (`row`, `col-*`, `btn`, `card`, `list-group`, etc.) with Tailwind utility classes
- Used custom Tailwind components (`.card-neon`, `.btn-success`, `.btn-primary`, etc.) for consistent retro neon styling
- Maintained backward compatibility with button class names (btn-success, btn-primary, btn-info, btn-danger)
- All templates now use:
  - Tailwind utility classes for layout and spacing
  - Custom neon color classes and components
  - Alpine.js for interactive elements (already in base.html)
  - Consistent retro neon aesthetic throughout

**Docker Integration:**
- Updated `compose/local/django/Dockerfile` to install Node.js and build Tailwind CSS during Docker build
- CSS is now built automatically when the container is built

**Note:** Allauth templates (third-party) still contain some Bootstrap classes but are functional. These can be customized separately if needed.

## 2024-12-19 - Switched to Tailwind CSS Play CDN for Testing

### User Request
please review the homepage styling, it may still be expecting bootstrap.
Also, let's try using the Play CDN option for TailwindCSS for testing: https://tailwindcss.com/docs/installation/play-cdn

### Response
Switched from compiled CSS to Tailwind CSS Play CDN for easier testing and development:

1. **Updated base.html:**
   - Replaced static CSS file link with Tailwind Play CDN script: `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`
   - Added inline `<style type="text/tailwindcss">` block with:
     - `@theme` configuration for custom neon colors
     - Custom CSS classes for neon colors (text-neon-cyan, border-neon-cyan, etc.)
     - Custom component classes (btn-success, btn-primary, card-neon, etc.) using regular CSS instead of @apply for Play CDN compatibility
     - Hover states for custom colors
     - Base styles for dark theme

2. **Homepage Review:**
   - Verified homepage template uses Tailwind classes correctly
   - All custom classes (text-neon-cyan, card-neon, btn-primary, etc.) are now defined in the inline styles
   - No Bootstrap classes remain in the homepage template

3. **Benefits of Play CDN:**
   - No build step required - works immediately
   - Perfect for testing and development
   - All Tailwind utilities work out of the box
   - Custom styles defined inline for easy modification

**Note:** The Play CDN is for development/testing only. For production, you should switch back to the compiled CSS approach for better performance.

## 2024-12-19 - Added Complete CRUD Views and Dashboard Enhancements

### User Request
We need to be able to create data. Please add CRUD views for all model types. Also, on the dashboard, add a "Create <object>" button next to the "View All" for each type. For example, under Companies, we would add a "Create Company" that loads the create company view/form.

Also, each of the list view templates should feature a "Back to homepage" link that goes back to the home page dashboard.

### Response
Implemented complete CRUD functionality for all models and enhanced the dashboard:

1. **Added UpdateView and DeleteView for all models:**
   - Sources app: CompanyUpdateView, CompanyDeleteView, ProductUpdateView, ProductDeleteView, BankUpdateView, BankDeleteView, SoundSourceUpdateView, SoundSourceDeleteView
   - Games app: GameUpdateView, GameDeleteView, GameTagUpdateView, GameTagDeleteView
   - Songs app: SongUpdateView, SongDeleteView, PersonUpdateView, PersonDeleteView

2. **Updated URL patterns:**
   - Added URL routes for all update and delete views in sources, games, and songs apps
   - All URLs follow consistent patterns: `<model>/<pk>/update/` and `<model>/<pk>/delete/`

3. **Enhanced dashboard (home.html):**
   - Added "Create <object>" buttons next to each "View All" button in the statistics cards
   - Buttons only show for authenticated users
   - Each card now has both "View All" (btn-primary) and "Create <object>" (btn-success) buttons side by side

4. **Updated all list view templates:**
   - Added "Back to homepage" link at the top of each list view template
   - Link uses neon-cyan color with hover effect
   - Consistent placement across all 8 list templates (company_list, product_list, bank_list, soundsource_list, game_list, gametag_list, song_list, person_list)

5. **Updated form templates:**
   - All form templates now handle both create and update modes
   - Dynamic titles and button text based on whether object.pk exists
   - Update forms use btn-info (neon-blue) while create forms use btn-success (neon-green)
   - Templates check `{% if object.pk %}` to determine mode

6. **Created delete confirmation templates:**
   - Created 8 delete confirmation templates (one for each model)
   - All follow consistent styling with warning message and cancel/delete buttons
   - Delete buttons use btn-danger (neon-pink) styling
   - Cancel buttons link back to the detail view

All CRUD operations are now fully functional with proper authentication requirements and consistent styling throughout the application.

## 2024-12-19 - Removed Email Requirement for User Registration

### User Request
remove the requirement for an email when creating new user accounts

### Response
Removed the email requirement from user account creation by making the following changes:

1. **Updated Django-allauth settings (`config/settings/base.py`):**
   - Removed `"email*"` from `ACCOUNT_SIGNUP_FIELDS` - changed from `["email*", "username*", "password1*", "password2*"]` to `["username*", "password1*", "password2*"]`
   - Changed `ACCOUNT_EMAIL_VERIFICATION` from `"mandatory"` to `"none"` to disable email verification since email is no longer required

2. **Updated User model (`vgm_source_database/users/models.py`):**
   - Added explicit `email` field override with `blank=True` to ensure email is optional
   - Imported `EmailField` from `django.db.models`
   - The email field was already set to `blank=True` in the migration, but explicitly overriding it in the model ensures consistency

**Changes Made:**
- Users can now create accounts with only username and password
- Email field is optional and can be left blank
- Email verification is disabled since email is not required
- The database schema already supported blank emails (from initial migration), so no new migration is needed

**Note:** Existing users with emails are unaffected. New users can choose to provide an email or leave it blank.

## 2024-12-19 - Enhanced Recent Activity Section to Show All CRUD Actions

### User Request
Review the code for the Recent Activity section of the dashboard. We want to see all CRUD actions, with creates and updates displaying the object as a Link to easily reach the detail page of newly created and modified objects. Limit the list to the last 15 operations

### Response
Enhanced the Recent Activity section to track all CRUD operations (Create and Update) across all models:

1. **Updated HomeView (`vgm_source_database/views.py`):**
   - Added imports for all models: Bank, GameTag, and Person (previously missing)
   - Created helper function `add_activity_items()` to track both creates and updates
   - Tracks creates using `created_at` timestamp
   - Tracks updates using `updated_at` timestamp (only when `updated_at > created_at` to avoid duplicates)
   - Includes all 8 model types: Company, Product, Bank, SoundSource, Game, GameTag, Song, Person
   - Changed limit from 10 to 15 operations
   - Each activity item includes:
     - `action`: "Created" or "Updated"
     - `type`: Model name (e.g., "Company", "Game")
     - `name`: Display name of the object
     - `url`: Link to the object's detail page
     - `timestamp`: When the action occurred

2. **Updated Template (`vgm_source_database/templates/pages/home.html`):**
   - Updated to display action type with color-coded badges:
     - "Created" actions use neon-green border and text
     - "Updated" actions use neon-cyan border and text
   - Changed timestamp field from `created_at` to `timestamp` to support both creates and updates
   - All activity items remain clickable links to their detail pages
   - Action badge appears alongside the model type badge

**Key Features:**
- Tracks both Create and Update operations across all models
- All creates and updates are clickable links to detail pages
- Color-coded action badges for easy visual distinction
- Limited to the last 15 operations sorted by timestamp
- Comprehensive coverage of all model types in the database

**Note:** Delete operations are not tracked since Django removes deleted objects from the database. To track deletes, an audit log system would need to be implemented.

## 2024-12-19 - Updated Theme from Neon Retro to Modern Dark Theme

### User Request
The neon theme is a bit too loud and too retro. Let's update to a more modern dark theme with some color - you can use this site as a reference: https://syntax.tailwindui.com/

### Response
Successfully migrated the theme from retro neon to a modern dark theme with subtle color accents, inspired by modern documentation sites like syntax.tailwindui.com.

**Changes Made:**

1. **Tailwind Configuration (`tailwind.config.js`):**
   - Removed all neon color definitions and glow effects
   - Updated dark theme colors to modern grays:
     - Background: `#111827` (gray-900)
     - Surface: `#1f2937` (gray-800)
     - Card: `#374151` (gray-700)
     - Border: `#4b5563` (gray-600)
   - Added modern accent colors:
     - Primary: `#3b82f6` (blue-500)
     - Success: `#10b981` (emerald-500)
     - Info: `#06b6d4` (cyan-500)
     - Danger: `#ef4444` (red-500)
     - Warning: `#f59e0b` (amber-500)
   - Replaced neon glow shadows with subtle modern shadows (soft, medium, large)
   - Removed all neon-specific animations and keyframes

2. **CSS Styling (`vgm_source_database/static/css/input.css`):**
   - Updated body background to modern dark gray (`#111827`)
   - Replaced all neon button classes with modern solid buttons:
     - `btn-success`: emerald-600 background with hover state
     - `btn-primary`: blue-600 background with hover state
     - `btn-info`: cyan-600 background with hover state
     - `btn-danger`: red-600 background with hover state
   - Removed monospace fonts and uppercase styling from buttons
   - Updated cards to use subtle borders instead of glowing neon borders
   - Modernized alerts with subtle borders and muted colors
   - Updated navigation links to use modern hover states (blue-400)
   - Updated form inputs with modern focus states
   - Removed all text glow utilities

3. **Base Template (`vgm_source_database/templates/base.html`):**
   - Updated theme variables to modern dark theme colors
   - Replaced all neon color utilities with modern color system
   - Updated button components to use solid backgrounds instead of transparent with borders
   - Removed all neon glow effects and animations
   - Updated navigation bar:
     - Removed neon cyan borders and shadows
     - Updated logo to use blue-400 instead of neon cyan
     - Removed monospace and uppercase styling
   - Updated alerts to use modern styling with subtle borders
   - Removed all text glow utilities

4. **Button Styling Rule (`.cursor/rules/general/button-styling.mdc`):**
   - Updated documentation to reflect modern dark theme
   - Changed descriptions from "neon" to "modern dark theme"
   - Updated color mappings to reference modern Tailwind colors (emerald-600, blue-600, cyan-600, red-600)
   - Removed references to glow effects

**Key Improvements:**
- More professional and modern appearance
- Better readability with subtle colors instead of bright neon
- Cleaner button design with solid backgrounds
- Subtle shadows and borders instead of glowing effects
- Modern sans-serif typography throughout
- Consistent with contemporary dark theme design patterns

**Color Scheme:**
- Background: Dark gray (#111827)
- Surfaces: Medium gray (#1f2937, #374151)
- Borders: Light gray (#4b5563)
- Accents: Muted blues, greens, cyans, and reds
- Text: Light gray with blue accents on hover

The theme now provides a clean, modern dark interface that's easier on the eyes while maintaining clear visual hierarchy and color coding for different action types.

## 2024-12-19 - Fixed SoundSource Validation to Allow Both Product and Bank

### User Request
I'm seeing this error when creating a sound source: "Sound source must have either a bank OR a product, not both."

This is actually not what we want. A sound source should be able to have either a Product and no Bank, or have both. Banks CAN be part of a product.

### Response
Fixed the validation logic in the `SoundSource` model to allow both a product and a bank to be set. The previous validation incorrectly prevented this combination.

**Changes Made:**
- Updated `SoundSource.clean()` method in `vgm_source_database/sources/models.py`
- Removed the validation check that prevented both bank and product from being set
- Kept the validation that ensures at least one of bank or product is set
- Updated the docstring to reflect the new validation rules

**Valid Sound Source Configurations:**
1. Product only (no Bank) ✓
2. Product + Bank (both) ✓ (now allowed)

The validation now correctly allows sound sources to have both a product and a bank, since banks are part of products and it makes sense to specify both for clarity and data integrity.

## 2024-12-19 - Fixed Form Styling for Dark Theme

### User Request
The forms look pretty ugly and some of the dropdowns show white text on a white background. Let's pretty up the form elements and also make sure the form field backgrounds are dark with lighter text.

### Response
Added comprehensive dark theme styling for all form elements to fix visibility issues and improve the overall appearance of forms.

**Solution:**
- Added extensive CSS styling to `base.html` to override Bootstrap5 form classes for dark theme compatibility
- All form elements now have dark backgrounds (#374151) with light text (#f3f4f6)
- Fixed dropdown/select elements to have proper dark styling with visible text
- Added styling for all form components: inputs, selects, textareas, checkboxes, radio buttons, labels, help text, and error messages

**Technical Details:**
- Styled `.form-control`, `.form-select`, and `select` elements with dark backgrounds and light text
- Added focus states with blue accent color and subtle box shadows
- Styled select dropdown options to have dark backgrounds
- Added proper styling for form labels, help text, and error messages
- Styled checkboxes and radio buttons with dark theme
- Added validation states (is-invalid, is-valid) with appropriate colors
- Styled disabled and readonly form controls
- Added styling for input groups and form rows

**Key Features:**
- All form inputs have dark backgrounds (#374151) with light text (#f3f4f6)
- Dropdowns/selects are fully visible with dark backgrounds and light text
- Focus states use blue accent color (#3b82f6) with subtle glow
- Error messages use red accent color (#f87171)
- Success states use green accent color (#10b981)
- Placeholder text uses muted gray (#9ca3af)
- Consistent styling across all form elements (text inputs, selects, textareas, checkboxes, radio buttons)
- Proper disabled/readonly states with reduced opacity

## 2024-12-19 - Updated Form Field Backgrounds for Better Contrast

### User Request
The forms look a lot better - lets make the actual form field backgrounds the same color as the main content window background for some contrast with the rest of the form.

### Response
Updated form field backgrounds to match the main content window background (#111827) instead of the card background (#374151), creating better visual contrast between the form fields and the form card container.

**Changes Made:**
- Changed all form control backgrounds from `#374151` (card background) to `#111827` (main background)
- Updated text inputs, selects, textareas, checkboxes, and radio buttons
- Updated focus states to maintain the darker background
- Updated validation states (valid/invalid) to use the darker background
- Updated select dropdown options to use the darker background
- Updated disabled/readonly controls to use an even darker shade (#0f1419) for better visual distinction

**Result:**
- Form fields now stand out against the card background with better contrast
- Improved visual hierarchy makes it easier to identify input areas
- Maintains readability with light text on dark background
- Consistent styling across all form elements

## 2024-12-19 - Created Excel to YAML Conversion Plan

### User Request
We just built our import/export pipeline. We need to convert this xlsx file to yaml to be imported. Provide a plan, showing which columns map to which fields in which models.

Ignore the first tab (called "Rules") and focus on the ones named after popular video game franchises. The tabs roughly correspond to what we want our Tags to be for the games within.

Filename: NEWER VGM Sound Sources.xlsx

### Response
Created a comprehensive conversion plan document that outlines how to convert the Excel file to YAML fixtures for import.

**Solution:**
- Created `ai_docs/EXCEL_TO_YAML_CONVERSION_PLAN.md` with detailed mapping plan
- Documented assumptions about Excel structure (tabs = GameTags, rows = SoundSources or Games)
- Provided column-to-field mappings for all possible scenarios:
  - If rows represent SoundSources
  - If rows represent Games
  - If rows represent both (mixed data)
- Created examination script (`examine_excel_structure.py`) to analyze actual Excel structure
- Documented relationship resolution strategies for ForeignKeys and ManyToMany fields

**Key Mappings Identified:**

**For SoundSources (most likely):**
- Name/Sound Name → `name` (CharField)
- Bank → `bank` (ForeignKey to Bank)
- Product → `product` (ForeignKey to Product)
- Company → indirect (via Product)
- Games → `games` (ManyToMany to Game)
- Songs → `songs` (ManyToMany to Song)
- Notes/Description → `notes` (TextField)

**For Games (if present):**
- Title/Game Title → `title` (CharField)
- Release Date → `release_date` (DateField)
- Release Year → `release_year` (IntegerField)
- Album Artists → `album_artists` (ManyToMany to Person)
- Tag → `tags` (ManyToMany to GameTag - from tab name)
- Notes → `notes` (TextField)

**For GameTags:**
- Tab name → `name` (CharField)
- Auto-generated `slug` from name
- Optional `description`

**Next Steps:**
1. Run `examine_excel_structure.py` to analyze actual Excel file structure
2. Identify exact column names and data types
3. Create conversion script based on actual structure
4. Generate YAML fixtures following import order
5. Validate with `import_data --dry-run`

**Files Created:**
- `ai_docs/EXCEL_TO_YAML_CONVERSION_PLAN.md` - Comprehensive conversion plan
- `examine_excel_structure.py` - Script to analyze Excel file structure
- `test_excel.py` - Test script for Excel examination

**Result:**
- Detailed plan showing column-to-field mappings for all models
- Clear documentation of assumptions and next steps
- Scripts ready to examine actual Excel structure
- Plan accounts for all model relationships and dependencies

## 2024-12-19 - Updated Excel Conversion Plan and Created Conversion Script

### User Request
Rows are sound sources generally, however, game names also appear as rows before their related sound sources appear.

For example, on the Zelda tab on line 155, we see the start of The Legend of Zelda: The Wind Waker. The next line discusses the game further before finally starting the sources at line 157. Each game typically has a few sections, like the common "Stuff to Find" section. The next game starts with The Legend of Zelda: The Wind Waker HD (Nintendo Wii U) at line 346.

You should basically add everything between the game titles as sound sources for that game. If a line doesn't make sense, skip it and comment a list at the end of all the skipped lines and which tab they are on.

### Response
Updated the conversion plan and created a conversion script that handles the actual Excel structure where game titles appear as standalone rows and all rows between game titles become sound sources.

**Solution:**
- Updated `ai_docs/EXCEL_TO_YAML_CONVERSION_PLAN.md` with actual structure details
- Updated `ai_docs/COLUMN_MAPPING_SUMMARY.md` with correct row organization
- Created `convert_excel_to_yaml.py` conversion script that:
  - Identifies game title rows (standalone rows with game titles)
  - Groups all rows between game titles as sound sources for the previous game
  - Skips section headers (like "Stuff to Find")
  - Skips game description rows
  - Tracks all skipped lines with reasons and sheet names
  - Generates YAML fixtures in proper dependency order
  - Creates a skipped lines report at the end

**Key Features:**
- **Game Title Detection**: Identifies standalone rows with game titles (10+ chars, may contain colons, parentheses, platform names)
- **Sound Source Grouping**: All rows between game titles automatically assigned to the previous game
- **Smart Skipping**: Skips section headers, empty rows, and rows that don't make sense as sound sources
- **Relationship Resolution**: Automatically resolves ForeignKeys and ManyToMany relationships
- **Skipped Lines Report**: Generates `skipped_lines_report.txt` listing all skipped lines with reasons and sheet names

**Conversion Process:**
1. Process each sheet (skip "Rules")
2. Create GameTag from sheet name
3. Identify game title rows
4. Group rows between game titles as sound sources
5. Resolve all relationships (Company, Product, Bank, Game)
6. Generate YAML fixtures in dependency order
7. Generate skipped lines report

**Files Created:**
- `convert_excel_to_yaml.py` - Main conversion script
- Updated documentation files with actual structure

**Result:**
- Conversion script ready to process Excel file
- Handles game title rows and sound source grouping correctly
- Tracks and reports all skipped lines
- Generates proper YAML fixtures for import

## 2024-12-19 - Added CSV to YAML Conversion Script

### User Request
lets skip the xlsx since it is hard to deal with - instead, I have added a number of csvs that each correspond to one of the tabs in the original Excel file. Review these csv files and convert them to yaml imports instead. Each file corresponds to a Tag - Zelda, Mario, etc

Rows are sound sources generally, however, game names also appear as rows before their related sound sources appear.

For example, on the Zelda file on line 155, we see the start of The Legend of Zelda: The Wind Waker. The next line discusses the game further before finally starting the sources at line 157. Each game typically has a few sections, like the common "Stuff to Find" section. The next game starts with The Legend of Zelda: The Wind Waker HD (Nintendo Wii U) at line 346.

You should basically add everything between the game titles as sound sources for that game. If a line doesn't make sense, skip it and comment a list at the end of all the skipped lines and which tab they are on

### Response
Created a CSV to YAML conversion script that processes CSV files instead of Excel, handling the same structure where game titles appear as rows and sound sources appear between them.

**Solution:**
- Created `convert_csv_to_yaml.py` - CSV conversion script
  - Processes all CSV files matching `NEWER VGM Sound Sources - *.csv`
  - Extracts GameTag names from filenames (e.g., "Zelda", "Mario", "Capcom")
  - Detects game title rows (standalone rows with game titles)
  - Groups rows between game titles as sound sources for that game
  - Handles release dates in Product column
  - Skips section headers and invalid rows
  - Generates YAML fixtures in dependency order
  - Creates skipped lines report

**Key Features:**
- **Game Title Detection**: Identifies rows with game titles in "Company/Manufacturer" column
- **Release Date Handling**: Extracts release dates from Product column (e.g., "(Released: November 21, 1991)")
- **Sound Source Parsing**: Uses "Program" column as name, maps other columns to Company/Product/Bank
- **Smart Skipping**: Skips section headers, empty rows, and invalid rows
- **Relationship Resolution**: Automatically resolves ForeignKeys and ManyToMany relationships

**Files Created:**
- `convert_csv_to_yaml.py` - Main CSV conversion script

**Result:**
- CSV conversion script ready to process all CSV files
- Handles the same structure as Excel (game titles + sound sources)
- Generates proper YAML fixtures for import

## 2024-12-19 - Added Import Data Functionality to GUI

### User Request
I have the import files now. We need a way in the gui to import these files. Please add a button (or more if there are multiple import types) to the sidebar, in a section beneath "Top Categories" - call this section "Data Management"

### Response
Added import functionality to the GUI with a new "Data Management" section in the sidebar.

**Solution:**
1. **Created Import Form** (`vgm_source_database/forms.py`):
   - `ImportDataForm` with file upload field for YAML fixtures
   - Includes "Dry Run" checkbox for validation without importing
   - File input accepts .yaml and .yml files

2. **Created Import View** (`vgm_source_database/views.py`):
   - `ImportDataView` - FormView for handling file uploads
   - Requires authentication (LoginRequiredMixin)
   - Handles file upload, saves to temporary file
   - Supports dry-run validation using `import_data` command
   - Performs actual import using `loaddata` command
   - Shows success/error messages to user
   - Cleans up temporary files

3. **Created Import Template** (`vgm_source_database/templates/pages/import_data.html`):
   - Form for uploading YAML fixture files
   - Instructions for users
   - Uses crispy forms for styling
   - Matches site's dark theme

4. **Added URL Routing**:
   - Created `vgm_source_database/urls.py` with import route
   - Added to main `config/urls.py` at `/import/`
   - Namespace: `data`

5. **Updated Sidebar** (`vgm_source_database/templates/base.html`):
   - Added "Data Management" section below "Top Categories"
   - Styled consistently with existing sidebar
   - "Import YAML" button (only visible to authenticated users)
   - Shows "Sign in to import data" for unauthenticated users

**Key Features:**
- **File Upload**: Users can upload YAML fixture files through the web interface
- **Dry Run Support**: Validate files before importing
- **Error Handling**: Clear error messages if import fails
- **Authentication Required**: Only authenticated users can import data
- **Consistent Styling**: Matches site's dark theme and button styles

**Files Created:**
- `vgm_source_database/forms.py` - Import form
- `vgm_source_database/urls.py` - URL routing for data management
- `vgm_source_database/templates/pages/import_data.html` - Import page template

**Files Modified:**
- `vgm_source_database/views.py` - Added ImportDataView
- `vgm_source_database/templates/base.html` - Added Data Management section to sidebar
- `config/urls.py` - Added import URL routing

**Result:**
- Import functionality accessible from sidebar
- Users can upload and import YAML fixture files through the GUI
- Dry-run validation available before actual import
- Clean, user-friendly interface matching site design

## 2024-12-19 - Fixed Fixture Import Error: Model Reference Format

### User Request
The importer's dry run says it's valid, but the import always fails with: "Error importing file: Problem installing fixture '/tmp/tmprqavtq06.yaml': Error deserializing object: too many values to unpack (expected 2)"

### Response
Fixed the model reference format in the YAML fixture generation. Django's fixture loader expects model references in the format `app_label.ModelName` (exactly 2 parts when split by '.'), but the converter was generating `vgm_source_database.app.ModelName` (3 parts), causing the unpacking error.

**Solution:**
1. Updated `convert_csv_to_yaml.py` to use correct model format:
   - Changed `vgm_source_database.games.GameTag` → `games.GameTag`
   - Changed `vgm_source_database.games.Game` → `games.Game`
   - Changed `vgm_source_database.sources.Company` → `sources.Company`
   - Changed `vgm_source_database.sources.Product` → `sources.Product`
   - Changed `vgm_source_database.sources.Bank` → `sources.Bank`
   - Changed `vgm_source_database.sources.SoundSource` → `sources.SoundSource`

2. Enhanced dry-run validation in `ImportDataView` to validate Django fixture format:
   - Checks that each item has required keys: `model`, `pk`, `fields`
   - Validates that `model` field is in correct format (exactly 2 parts: `app_label.ModelName`)
   - Validates that `fields` is a dictionary
   - Provides specific error messages indicating which item and what's wrong

**Files Modified:**
- `convert_csv_to_yaml.py` - Fixed all model reference formats (6 occurrences)
- `vgm_source_database/views.py` - Enhanced dry-run validation to check Django fixture format

**Result:**
- Fixtures now use correct Django format (`app_label.ModelName`)
- Dry-run validation now catches format errors before import
- Import should now work correctly for newly generated fixtures
- Existing fixtures with wrong format will need to be regenerated

## 2024-12-19 - Fixed Missing created_at and updated_at Fields in Fixtures

### User Request
Product import failed with: "null value in column 'created_at' of relation 'sources_product' violates not-null constraint". The dry run passed, but actual import failed.

### Response
Fixed missing `created_at` and `updated_at` fields in generated fixtures. Django's `loaddata` command doesn't automatically populate `auto_now_add` and `auto_now` fields when they're missing from fixtures, causing NOT NULL constraint violations.

**Solution:**
1. Added `datetime` and `timezone` imports to `convert_csv_to_yaml.py`
2. Added `created_at` and `updated_at` fields to all model fixtures:
   - GameTag
   - Game
   - Company
   - Product
   - Bank
   - SoundSource
3. Used UTC timezone-aware datetime in ISO format (Django's preferred format)

**Files Modified:**
- `convert_csv_to_yaml.py` - Added datetime imports and timestamp fields to all fixture generation

**Result:**
- All generated fixtures now include required timestamp fields
- Import should now work without constraint violations
- Timestamps use proper ISO format with UTC timezone

## 2024-12-19 - Fixed Unicode Characters in GameTag Slugs

### User Request
Games import failed with: "NoReverseMatch: Reverse for 'gametag_detail' with arguments '('pokémon',)' not found". The slug "pokémon" contains a Unicode character (é) that doesn't match the URL pattern which only allows ASCII characters.

### Response
Fixed the slugify function to normalize Unicode characters to their ASCII equivalents. The URL pattern `[-a-zA-Z0-9_]+` only accepts ASCII characters, but the slug "pokémon" contains a Unicode character.

**Solution:**
1. Added `unicodedata` import to handle Unicode normalization
2. Updated `slugify()` method to:
   - Normalize Unicode characters using NFKD normalization
   - Convert to ASCII by removing combining characters (diacritics)
   - Convert é → e, ñ → n, etc.
   - Ensure only ASCII alphanumeric characters, underscores, and hyphens remain

**Files Modified:**
- `convert_csv_to_yaml.py` - Enhanced slugify function with Unicode normalization

**Result:**
- Unicode characters in GameTag names are now converted to ASCII in slugs
- "pokémon" → "pokemon" (matches URL pattern)
- Slugs now work correctly with Django URL routing

### Immediate Fix for Existing Database
Created two tools to fix existing broken slugs in the database:
1. **Quick fix script** (`fix_slugs_now.py`) - Run immediately to fix all slugs
2. **Management command** (`fix_gametag_slugs`) - Reusable command for future use

Both tools use the same Unicode normalization logic to regenerate slugs.

## 2024-12-19 - Fixed Missing Fallback Products in Fixtures

### User Request
Sources import failed with foreign key constraint violation: SoundSource references Product pk=1719 that doesn't exist in the database.

### Response
Fixed missing fallback products in generated fixtures. When a SoundSource doesn't have a valid product, the code creates a fallback product using the company name, but these fallback products were being created AFTER the products_yaml was generated, so they weren't included in the fixture file.

**Solution:**
1. Moved fallback product creation from `generate_yaml()` to `resolve_relationships()`
2. Fallback products are now created before products_yaml generation
3. All products (including fallbacks) are now included in the YAML fixture

**Files Modified:**
- `convert_csv_to_yaml.py` - Moved fallback product creation to resolve_relationships()

**Result:**
- All fallback products are now included in fixtures
- Foreign key constraints are satisfied
- SoundSources can reference fallback products that exist in the database

## 2024-12-19 - Added Combined Fixture File Option

### User Request
Is there any way to generate a single import file so I don't have to keep doing a bunch of imports in the right order one at a time?

### Response
Added support for generating a single combined fixture file that contains all models in the correct dependency order. This allows importing everything with a single command instead of multiple imports.

**Solution:**
1. Added `combined_file` parameter to `CSVConverter.__init__()`
2. Modified `generate_yaml()` to optionally combine all fixtures into one file
3. Added command-line argument `--combined` to the converter script
4. Combined file is named `all_fixtures.yaml` and contains all models in dependency order:
   - GameTags (no dependencies)
   - Companies (no dependencies)
   - Products (depends on Companies)
   - Banks (depends on Products)
   - Games (depends on GameTags)
   - SoundSources (depends on Banks, Products, Games)

**Usage:**
```bash
# Generate combined file
python convert_csv_to_yaml.py --combined

# Or with custom directories
python convert_csv_to_yaml.py --csv-dir dev_reference --output-dir fixtures --combined
```

**Files Modified:**
- `convert_csv_to_yaml.py` - Added combined file support

**Result:**
- Single `all_fixtures.yaml` file can be imported with one command
- All models included in correct dependency order
- No need to import multiple files in sequence

## 2024-12-19 - Added Duplicate Handling to Importer

### User Request
The importer errors out when duplicates are hit. Update importer logic to simply skip duplicates or provide an option to overwrite them.

### Response
Added duplicate handling to both the web import view and management command. Users can now choose to skip duplicates (keep existing) or overwrite them (update existing).

**Solution:**
1. Created `import_utils.py` with custom import function that handles duplicates
2. Added `duplicate_handling` field to `ImportDataForm` with choices: "skip" or "overwrite"
3. Updated `ImportDataView` to use custom import function with statistics
4. Updated `import_data` management command to support `--duplicate-handling` option
5. Import function properly handles ManyToMany fields and ForeignKey relationships

**Features:**
- **Skip duplicates (default)**: Keeps existing objects, only creates new ones
- **Overwrite duplicates**: Updates existing objects with new data from fixture
- **Statistics reporting**: Shows created, updated, skipped counts
- **Error handling**: Gracefully handles IntegrityError and other exceptions

**Files Created:**
- `vgm_source_database/import_utils.py` - Custom import function with duplicate handling

**Files Modified:**
- `vgm_source_database/forms.py` - Added duplicate_handling field
- `vgm_source_database/views.py` - Updated to use custom import function
- `config/management/commands/import_data.py` - Added duplicate handling option

**Usage:**
```bash
# Skip duplicates (default)
python manage.py import_data --file fixtures/all_fixtures.yaml

# Overwrite duplicates
python manage.py import_data --file fixtures/all_fixtures.yaml --duplicate-handling overwrite
```

**Result:**
- Imports no longer fail on duplicates
- Users can choose to skip or overwrite existing data
- Detailed statistics show what was imported
- Better error handling and reporting

