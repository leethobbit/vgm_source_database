"""Convert CSV files to YAML fixtures for VGM Source Database.

Each CSV file corresponds to a GameTag (e.g., "Zelda", "Mario").
Game titles appear as rows, and sound sources appear as rows between game titles.
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Install with: pip install pyyaml")
    sys.exit(1)


class CSVConverter:
    """Convert CSV files to YAML fixtures."""

    def __init__(self, csv_dir: str, output_dir: str = "fixtures"):
        """Initialize converter.

        Args:
            csv_dir: Directory containing CSV files
            output_dir: Directory to write YAML files
        """
        self.csv_dir = Path(csv_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Track all objects for relationship resolution
        self.gametags: Dict[str, Dict] = {}  # name -> {pk, slug}
        self.companies: Dict[str, int] = {}  # name -> pk
        self.products: Dict[Tuple[str, str], int] = {}  # (name, company_name) -> pk
        self.banks: Dict[Tuple[str, str, str], int] = {}  # (name, product_name, company_name) -> pk
        self.games: Dict[str, int] = {}  # title -> pk
        self.game_to_tag: Dict[str, str] = {}  # game_title -> tag_name

        # Track skipped lines
        self.skipped_lines: List[Dict[str, Any]] = []

        # PK counters
        self.gametag_pk = 1
        self.company_pk = 1
        self.product_pk = 1
        self.bank_pk = 1
        self.game_pk = 1
        self.soundsource_pk = 1

        # All games and sound sources
        self.all_games: List[Dict] = []
        self.all_sound_sources: List[Dict] = []

    def slugify(self, text: str) -> str:
        """Convert text to slug.

        Args:
            text: Text to slugify

        Returns:
            Slugified text
        """
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)
        return text

    def is_game_title_row(self, row: Dict[str, str]) -> bool:
        """Check if a row represents a game title.

        Args:
            row: Dictionary of row data

        Returns:
            True if row appears to be a game title
        """
        # Game titles typically have:
        # - Company/Manufacturer column empty or has special patterns
        # - Product column empty
        # - First column (Company) has the game title
        company = row.get("Company/Manufacturer", "").strip()
        product = row.get("Product", "").strip()
        path_bank = row.get("Path/Bank", "").strip()
        program = row.get("Program", "").strip()

        if not company:
            return False

        # Skip section headers
        section_patterns = [
            "STUFF TO FIND",
            "SOURCES",
            "NOTES",
            "DESCRIPTION",
            "TABLE OF CONTENTS",
            "JUMP TO:",
            "SECTION",
            "BASE GAME",
        ]
        if any(pattern in company.upper() for pattern in section_patterns):
            return False

        # Skip empty rows and metadata
        if company.startswith("Please remember") or company.startswith("(Click"):
            return False

        # Game titles typically:
        # - Are 10+ characters
        # - Don't have Product/Path/Bank/Program filled (or very minimal)
        # - May contain colons, parentheses, platform names
        if len(company) < 10:
            return False

        # Check if Product column contains release date (common pattern)
        has_release_date = bool(re.search(r"\(Released:", product, re.IGNORECASE)) if product else False
        
        # If Product, Path/Bank, and Program are all empty (or Product just has release date), likely a game title
        if (not product or has_release_date) and not path_bank and not program:
            # Check for game indicators
            game_indicators = [
                ":",
                "(",
                "HD",
                "Remaster",
                "Remake",
                "Edition",
                "Wii",
                "PlayStation",
                "Xbox",
                "Nintendo",
                "PC",
                "Switch",
                "3DS",
                "GameCube",
                "Arcade",
                "SNES",
                "N64",
                "★",  # Star symbols used in game titles
            ]
            if any(indicator in company for indicator in game_indicators):
                return True

            # Long standalone text (20+ chars) is likely a game title
            if len(company) >= 20:
                return True

        # Sometimes game titles have minimal info in other columns (like release date)
        # Check if other columns are minimal/descriptive
        other_cols_filled = sum(1 for col in [product, path_bank, program] if col and len(col) > 5 and not has_release_date)
        if other_cols_filled <= 1 and len(company) >= 15:
            # Might be a game title with release info
            return True

        return False

    def is_section_header(self, row: Dict[str, str]) -> bool:
        """Check if a row is a section header to skip.

        Args:
            row: Dictionary of row data

        Returns:
            True if row is a section header
        """
        company = row.get("Company/Manufacturer", "").strip().upper()
        section_patterns = [
            "STUFF TO FIND",
            "SOURCES",
            "NOTES",
            "DESCRIPTION",
            "TABLE OF CONTENTS",
            "JUMP TO:",
            "SECTION",
            "BASE GAME",
            "PLEASE REMEMBER",
        ]
        return any(pattern in company for pattern in section_patterns)

    def parse_sound_source_row(
        self, row: Dict[str, str], current_game_title: str
    ) -> Optional[Dict[str, Any]]:
        """Parse a row as a sound source.

        Args:
            row: Dictionary of row data
            current_game_title: Title of current game

        Returns:
            Dictionary of sound source data or None if invalid
        """
        company = row.get("Company/Manufacturer", "").strip()
        product = row.get("Product", "").strip()
        path_bank = row.get("Path/Bank", "").strip()
        program = row.get("Program", "").strip()
        notes = row.get("Notes", "").strip()
        examples = row.get("Examples", "").strip()

        # Skip if no company/product (not a valid sound source)
        if not company and not product:
            return None

        # Skip section headers
        if self.is_section_header(row):
            return None

        # Skip rows that look like game titles
        if self.is_game_title_row(row):
            return None

        # Sound source name is typically the Program column, or Company if Program is empty
        name = program if program else company
        if not name or len(name) < 2:
            return None

        # Build notes from multiple columns
        full_notes = []
        if notes:
            full_notes.append(notes)
        if examples:
            full_notes.append(f"Examples: {examples}")
        if path_bank and path_bank not in name:
            full_notes.append(f"Path/Bank: {path_bank}")

        sound_source = {
            "name": name,
            "company": company if company else None,
            "product": product if product else None,
            "bank": path_bank if path_bank else None,
            "games": [current_game_title] if current_game_title else [],
            "notes": " | ".join(full_notes) if full_notes else "",
        }

        return sound_source

    def process_csv_file(self, csv_file: Path) -> None:
        """Process a single CSV file.

        Args:
            csv_file: Path to CSV file
        """
        # Extract tag name from filename (e.g., "NEWER VGM Sound Sources - Zelda.csv" -> "Zelda")
        tag_name = csv_file.stem.replace("NEWER VGM Sound Sources - ", "").strip()
        if not tag_name:
            tag_name = csv_file.stem

        print(f"Processing: {csv_file.name} -> Tag: {tag_name}")

        # Create GameTag
        if tag_name not in self.gametags:
            self.gametags[tag_name] = {
                "pk": self.gametag_pk,
                "slug": self.slugify(tag_name),
            }
            self.gametag_pk += 1

        # Read CSV
        games = []
        sound_sources = []
        current_game_title = None
        current_game_data = None

        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            if not headers:
                print(f"  Warning: No headers found in {csv_file.name}")
                return

            for row_idx, row in enumerate(reader, start=2):  # Start at 2 (after header)
                # Check if game title
                if self.is_game_title_row(row):
                    # Save previous game
                    if current_game_title and current_game_data:
                        games.append(current_game_data)

                    # Start new game
                    game_title = row.get("Company/Manufacturer", "").strip()
                    if game_title:
                        current_game_title = game_title
                        current_game_data = {
                            "title": game_title,
                            "tags": [tag_name],
                            "release_date": None,
                            "release_year": None,
                            "album_artists": [],
                            "notes": "",
                        }

                        # Try to extract release year from title or other columns
                        year_match = re.search(r"\((\d{4})\)", game_title)
                        if not year_match:
                            # Check Product column for release date
                            product = row.get("Product", "").strip()
                            year_match = re.search(r"\((\d{4})\)", product)

                        if year_match:
                            try:
                                current_game_data["release_year"] = int(year_match.group(1))
                            except ValueError:
                                pass

                elif current_game_title:
                    # Try to parse as sound source
                    sound_source = self.parse_sound_source_row(row, current_game_title)

                    if sound_source:
                        sound_sources.append(sound_source)
                    else:
                        # Skip this row
                        company = row.get("Company/Manufacturer", "").strip()
                        if company:  # Only track non-empty rows
                            self.skipped_lines.append({
                                "file": csv_file.name,
                                "row": row_idx,
                                "content": company[:100],
                                "reason": "Could not parse as sound source or game title",
                            })

        # Save last game
        if current_game_title and current_game_data:
            games.append(current_game_data)

        self.all_games.extend(games)
        self.all_sound_sources.extend(sound_sources)

        print(f"  Found {len(games)} games, {len(sound_sources)} sound sources")

    def resolve_relationships(self) -> None:
        """Resolve ForeignKey and ManyToMany relationships."""
        # Create/get Game objects
        for game_data in self.all_games:
            title = game_data["title"]
            if title not in self.games:
                self.games[title] = self.game_pk
                self.game_to_tag[title] = game_data["tags"][0]  # Store tag for this game
                self.game_pk += 1

        # Create/get Company, Product, Bank objects
        for ss in self.all_sound_sources:
            if ss["company"]:
                company_name = ss["company"]
                if company_name not in self.companies:
                    self.companies[company_name] = self.company_pk
                    self.company_pk += 1

            if ss["product"] and ss["company"]:
                product_name = ss["product"]
                company_name = ss["company"]
                key = (product_name, company_name)
                if key not in self.products:
                    self.products[key] = self.product_pk
                    self.product_pk += 1

            if ss["bank"] and ss["product"] and ss["company"]:
                bank_name = ss["bank"]
                product_name = ss["product"]
                company_name = ss["company"]
                key = (bank_name, product_name, company_name)
                if key not in self.banks:
                    self.banks[key] = self.bank_pk
                    self.bank_pk += 1

    def generate_yaml(self) -> None:
        """Generate YAML fixture files."""
        # 1. GameTags
        gametags_yaml = []
        for name, data in sorted(self.gametags.items()):
            gametags_yaml.append({
                "model": "vgm_source_database.games.GameTag",
                "pk": data["pk"],
                "fields": {
                    "name": name,
                    "slug": data["slug"],
                    "description": "",
                },
            })

        # 2. Companies
        companies_yaml = []
        for name, pk in sorted(self.companies.items()):
            companies_yaml.append({
                "model": "vgm_source_database.sources.Company",
                "pk": pk,
                "fields": {
                    "name": name,
                    "notes": "",
                },
            })

        # 3. Products
        products_yaml = []
        for (name, company_name), pk in sorted(self.products.items()):
            company_pk = self.companies.get(company_name)
            if company_pk:
                products_yaml.append({
                    "model": "vgm_source_database.sources.Product",
                    "pk": pk,
                    "fields": {
                        "name": name,
                        "company": company_pk,
                        "notes": "",
                    },
                })

        # 4. Banks
        banks_yaml = []
        for (name, product_name, company_name), pk in sorted(self.banks.items()):
            product_key = (product_name, company_name)
            product_pk = self.products.get(product_key)
            if product_pk:
                banks_yaml.append({
                    "model": "vgm_source_database.sources.Bank",
                    "pk": pk,
                    "fields": {
                        "name": name,
                        "product": product_pk,
                        "notes": "",
                    },
                })

        # 5. Games
        games_yaml = []
        for game_data in self.all_games:
            title = game_data["title"]
            game_pk = self.games.get(title)
            if game_pk:
                # Resolve tag PKs
                tag_pks = []
                for tag_name in game_data["tags"]:
                    if tag_name in self.gametags:
                        tag_pks.append(self.gametags[tag_name]["pk"])

                games_yaml.append({
                    "model": "vgm_source_database.games.Game",
                    "pk": game_pk,
                    "fields": {
                        "title": title,
                        "release_date": game_data["release_date"],
                        "release_year": game_data["release_year"],
                        "album_artists": [],
                        "tags": tag_pks,
                        "notes": game_data["notes"] or "",
                    },
                })

        # 6. SoundSources
        soundsources_yaml = []
        for ss in self.all_sound_sources:
            # Resolve bank/product
            bank_pk = None
            product_pk = None

            if ss["bank"] and ss["product"] and ss["company"]:
                bank_key = (ss["bank"], ss["product"], ss["company"])
                bank_pk = self.banks.get(bank_key)

            if ss["product"] and ss["company"]:
                product_key = (ss["product"], ss["company"])
                product_pk = self.products.get(product_key)

            # At least one must be set
            if not bank_pk and not product_pk:
                # Try to create product from company if available
                if ss["company"]:
                    company_name = ss["company"]
                    if company_name in self.companies:
                        # Use company as product fallback
                        product_key = (company_name, company_name)
                        if product_key not in self.products:
                            self.products[product_key] = self.product_pk
                            product_pk = self.product_pk
                            self.product_pk += 1
                        else:
                            product_pk = self.products[product_key]

            if not bank_pk and not product_pk:
                # Skip this sound source - invalid
                continue

            # Resolve game PKs
            game_pks = []
            for game_title in ss["games"]:
                if game_title in self.games:
                    game_pks.append(self.games[game_title])

            soundsources_yaml.append({
                "model": "vgm_source_database.sources.SoundSource",
                "pk": self.soundsource_pk,
                "fields": {
                    "name": ss["name"],
                    "bank": bank_pk,
                    "product": product_pk,
                    "discoverers": [],
                    "games": game_pks,
                    "songs": [],
                    "notes": ss["notes"] or "",
                },
            })
            self.soundsource_pk += 1

        # Write YAML files
        files_to_write = [
            ("games_gametags.yaml", gametags_yaml),
            ("sources_companies.yaml", companies_yaml),
            ("sources_products.yaml", products_yaml),
            ("sources_banks.yaml", banks_yaml),
            ("games_games.yaml", games_yaml),
            ("sources_soundsources.yaml", soundsources_yaml),
        ]

        for filename, data in files_to_write:
            filepath = self.output_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"Generated: {filepath} ({len(data)} entries)")

        # Write skipped lines report
        if self.skipped_lines:
            report_path = self.output_dir / "skipped_lines_report.txt"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("SKIPPED LINES REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Total skipped lines: {len(self.skipped_lines)}\n\n")

                # Group by file
                by_file = defaultdict(list)
                for item in self.skipped_lines:
                    by_file[item["file"]].append(item)

                for file_name, items in sorted(by_file.items()):
                    f.write(f"\nFile: {file_name}\n")
                    f.write("-" * 60 + "\n")
                    for item in items:
                        f.write(f"  Row {item['row']}: {item['content']}\n")
                        f.write(f"    Reason: {item['reason']}\n")

            print(f"\nSkipped lines report: {report_path} ({len(self.skipped_lines)} lines)")

    def convert(self) -> None:
        """Main conversion method."""
        # Write status to file immediately
        status_file = self.output_dir / "conversion_status.txt"
        with open(status_file, "w", encoding="utf-8") as f:
            f.write("Starting conversion...\n")
        
        csv_files = list(self.csv_dir.glob("NEWER VGM Sound Sources - *.csv"))
        
        with open(status_file, "a", encoding="utf-8") as f:
            f.write(f"CSV directory: {self.csv_dir}\n")
            f.write(f"Found {len(csv_files)} CSV files\n")

        if not csv_files:
            with open(status_file, "a", encoding="utf-8") as f:
                f.write(f"ERROR: No CSV files found in {self.csv_dir}\n")
            print(f"ERROR: No CSV files found in {self.csv_dir}")
            print(f"Expected files like: 'NEWER VGM Sound Sources - Zelda.csv'")
            sys.exit(1)

        print(f"Found {len(csv_files)} CSV files to process...\n")
        with open(status_file, "a", encoding="utf-8") as f:
            f.write(f"Processing {len(csv_files)} files...\n")

        for csv_file in sorted(csv_files):
            self.process_csv_file(csv_file)

        # Resolve relationships
        print("\nResolving relationships...")
        self.resolve_relationships()

        # Generate YAML
        print("\nGenerating YAML files...")
        self.generate_yaml()

        print(f"\nConversion complete!")
        print(f"  GameTags: {len(self.gametags)}")
        print(f"  Companies: {len(self.companies)}")
        print(f"  Products: {len(self.products)}")
        print(f"  Banks: {len(self.banks)}")
        print(f"  Games: {len(self.games)}")
        print(f"  SoundSources: {len(self.all_sound_sources)}")
        print(f"  Skipped lines: {len(self.skipped_lines)}")
        
        # Write final status
        status_file = self.output_dir / "conversion_status.txt"
        with open(status_file, "a", encoding="utf-8") as f:
            f.write(f"\nConversion complete!\n")
            f.write(f"  GameTags: {len(self.gametags)}\n")
            f.write(f"  Companies: {len(self.companies)}\n")
            f.write(f"  Products: {len(self.products)}\n")
            f.write(f"  Banks: {len(self.banks)}\n")
            f.write(f"  Games: {len(self.games)}\n")
            f.write(f"  SoundSources: {len(self.all_sound_sources)}\n")
            f.write(f"  Skipped lines: {len(self.skipped_lines)}\n")


if __name__ == "__main__":
    import traceback
    
    try:
        csv_dir = "dev_reference"
        output_dir = "fixtures"
        
        print("Initializing converter...")
        converter = CSVConverter(csv_dir, output_dir)
        
        print("Starting conversion...")
        converter.convert()
        
        print("Done!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        
        # Write error to file
        error_file = Path("fixtures") / "conversion_error.txt"
        error_file.parent.mkdir(exist_ok=True)
        with open(error_file, "w", encoding="utf-8") as f:
            f.write(f"ERROR: {e}\n")
            f.write(traceback.format_exc())
        
        sys.exit(1)
