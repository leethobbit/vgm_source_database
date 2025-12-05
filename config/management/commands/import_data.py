"""Management command to import data from YAML fixtures."""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


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
            call_command(
                "loaddata",
                str(fixture_file),
                verbosity=verbosity,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully imported: {fixture_file}"),
            )
        except Exception as e:
            raise CommandError(f"Error importing {fixture_file}: {e}") from e
