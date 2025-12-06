"""Management command to import data from YAML fixtures."""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from vgm_source_database.import_utils import import_fixture_file


class Command(BaseCommand):
    """Import database data from YAML fixtures.

    This command imports data from YAML fixture files into the database.
    It uses Django's built-in loaddata command which handles model dependencies
    and relationships automatically.

    Usage:
        python manage.py import_data [--fixture-dir fixtures] [--file FILE] [--dry-run]
    """

    help = "Import database data from YAML fixtures"

    def add_arguments(self, parser):
        """Add command arguments.

        Args:
            parser: Argument parser instance.
        """
        parser.add_argument(
            "--fixture-dir",
            type=str,
            default="fixtures",
            help="Directory containing fixture files (default: fixtures)",
        )
        parser.add_argument(
            "--file",
            type=str,
            help="Import a specific fixture file",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate fixtures without importing (read-only check)",
        )
        parser.add_argument(
            "--verbosity",
            type=int,
            default=1,
            help="Verbosity level (0=minimal, 1=normal, 2=verbose, 3=very verbose)",
        )
        parser.add_argument(
            "--duplicate-handling",
            type=str,
            choices=["skip", "overwrite"],
            default="skip",
            help="How to handle duplicates: 'skip' (keep existing) or 'overwrite' (update existing)",
        )
        parser.add_argument(
            "--error-file",
            type=str,
            help="File path to write error details (if errors occur)",
        )

    def handle(self, *args, **options):
        """Execute the import command.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.
        """
        fixture_dir = Path(options["fixture_dir"])

        if not fixture_dir.exists():
            raise CommandError(f"Fixture directory not found: {fixture_dir}")

        # Define import order (respecting dependencies)
        fixture_order = [
            "games_gametags.yaml",
            "games_games.yaml",
            "songs_people.yaml",
            "songs_songs.yaml",
            "sources_companies.yaml",
            "sources_products.yaml",
            "sources_banks.yaml",
            "sources_soundsources.yaml",
        ]

        if options["file"]:
            # Import single file
            fixture_file = Path(options["file"])
            if not fixture_file.exists():
                raise CommandError(f"Fixture file not found: {fixture_file}")

            self._import_file(fixture_file, options)
        else:
            # Import all files in order
            imported_count = 0
            for filename in fixture_order:
                fixture_file = fixture_dir / filename
                if fixture_file.exists():
                    self._import_file(fixture_file, options)
                    imported_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Fixture file not found: {fixture_file}, skipping..."),
                    )

            if imported_count == 0:
                self.stdout.write(
                    self.style.WARNING("No fixture files found to import."),
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"\nImport complete! Imported {imported_count} fixture files."),
                )

    def _import_file(self, fixture_file: Path, options: dict) -> None:
        """Import a single fixture file.

        Args:
            fixture_file: Path to fixture file.
            options: Command options dictionary.
        """
        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(f"[DRY RUN] Would import: {fixture_file}"),
            )
            # In dry-run mode, we could validate the YAML structure
            # For now, just report what would be imported
            return

        try:
            verbosity = options.get("verbosity", 1)
            duplicate_handling = options.get("duplicate_handling", "skip")
            
            stats = import_fixture_file(
                str(fixture_file),
                duplicate_handling=duplicate_handling,
                verbosity=verbosity,
            )
            
            # Report statistics
            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported: {fixture_file} - "
                    f"Total: {stats['total']}, "
                    f"Created: {stats['created']}, "
                    f"{'Updated' if duplicate_handling == 'overwrite' else 'Skipped'}: "
                    f"{stats['updated' if duplicate_handling == 'overwrite' else 'skipped']}"
                ),
            )
            
            if stats["errors"]:
                error_file = options.get("error_file")
                if error_file:
                    # Write errors to file
                    with open(error_file, "w", encoding="utf-8") as f:
                        f.write(f"Import Errors ({len(stats['errors'])} total)\n")
                        f.write("=" * 80 + "\n\n")
                        for error in stats["errors"]:
                            f.write(f"{error}\n")
                    self.stdout.write(
                        self.style.WARNING(
                            f"  {len(stats['errors'])} error(s) occurred. "
                            f"Details written to: {error_file}"
                        ),
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  {len(stats['errors'])} error(s) occurred. "
                            "Use --verbosity 2 to see details or --error-file to save to file."
                        ),
                    )
                if verbosity >= 2:
                    # Show first 50 errors in console
                    for error in stats["errors"][:50]:
                        self.stdout.write(self.style.ERROR(f"  - {error}"))
                    if len(stats["errors"]) > 50:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  ... and {len(stats['errors']) - 50} more errors. "
                                "Use --error-file to see all errors."
                            ),
                        )
                        
        except Exception as e:
            raise CommandError(f"Error importing {fixture_file}: {e}") from e
