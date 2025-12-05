"""Management command to export data to YAML fixtures."""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import serialize
from django.db import models

from vgm_source_database.games.models import Game, GameTag
from vgm_source_database.songs.models import Person, Song
from vgm_source_database.sources.models import Bank, Company, Product, SoundSource


class Command(BaseCommand):
    """Export database data to YAML fixtures.

    This command exports all data from the VGM Source Database models to YAML
    fixture files. The export respects model dependencies and exports data in
    the correct order for import.

    Usage:
        python manage.py export_data [--output-dir fixtures] [--app APP_NAME]
    """

    help = "Export database data to YAML fixtures"

    def add_arguments(self, parser):
        """Add command arguments.

        Args:
            parser: Argument parser instance.
        """
        parser.add_argument(
            "--output-dir",
            type=str,
            default="fixtures",
            help="Directory to save fixture files (default: fixtures)",
        )
        parser.add_argument(
            "--app",
            type=str,
            help="Export only a specific app (games, songs, sources)",
        )
        parser.add_argument(
            "--format",
            type=str,
            choices=["yaml", "json"],
            default="yaml",
            help="Output format (default: yaml)",
        )

    def handle(self, *args, **options):
        """Execute the export command.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.
        """
        output_dir = Path(options["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)

        app_filter = options.get("app")
        output_format = options["format"]

        # Define model export order (respecting dependencies)
        model_groups = {
            "games": [
                (GameTag, "gametags"),
                (Game, "games"),
            ],
            "songs": [
                (Person, "people"),
                (Song, "songs"),
            ],
            "sources": [
                (Company, "companies"),
                (Product, "products"),
                (Bank, "banks"),
                (SoundSource, "soundsources"),
            ],
        }

        exported_count = 0

        for app_name, models_list in model_groups.items():
            if app_filter and app_name != app_filter:
                continue

            for model_class, filename in models_list:
                try:
                    queryset = model_class.objects.all()
                    count = queryset.count()

                    if count == 0:
                        self.stdout.write(
                            self.style.WARNING(
                                f"No {model_class.__name__} objects found, skipping...",
                            ),
                        )
                        continue

                    # Serialize to JSON first (Django's built-in serializer)
                    json_data = serialize("json", queryset, use_natural_foreign_keys=True)

                    # Convert to Python objects
                    data = json.loads(json_data)

                    # Write to file
                    if output_format == "yaml":
                        output_file = output_dir / f"{app_name}_{filename}.yaml"
                        self._write_yaml(output_file, data)
                    else:
                        output_file = output_dir / f"{app_name}_{filename}.json"
                        self._write_json(output_file, data)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Exported {count} {model_class.__name__} objects to {output_file}",
                        ),
                    )
                    exported_count += count

                except Exception as e:
                    raise CommandError(f"Error exporting {model_class.__name__}: {e}") from e

        self.stdout.write(
            self.style.SUCCESS(f"\nExport complete! Exported {exported_count} total objects."),
        )

    def _write_yaml(self, output_file: Path, data: list) -> None:
        """Write data to YAML file.

        Args:
            output_file: Path to output file.
            data: List of serialized model objects.
        """
        try:
            import yaml
        except ImportError:
            raise CommandError(
                "PyYAML is required for YAML export. Install it with: pip install pyyaml",
            ) from None

        # Convert Django's serialization format to fixture format
        yaml_data = []
        for item in data:
            model_name = item["model"]
            fields = item["fields"]
            pk = item["pk"]

            # Convert to fixture format
            fixture_item = {
                "model": model_name,
                "pk": pk,
                "fields": fields,
            }
            yaml_data.append(fixture_item)

        with output_file.open("w", encoding="utf-8") as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    def _write_json(self, output_file: Path, data: list) -> None:
        """Write data to JSON file.

        Args:
            output_file: Path to output file.
            data: List of serialized model objects.
        """
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
