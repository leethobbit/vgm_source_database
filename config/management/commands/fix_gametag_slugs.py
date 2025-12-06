"""Management command to fix GameTag slugs with Unicode characters."""

import re
import unicodedata

from django.core.management.base import BaseCommand

from vgm_source_database.games.models import GameTag


def slugify_ascii(text: str) -> str:
    """Convert text to slug, normalizing Unicode characters to ASCII.

    Args:
        text: Text to slugify

    Returns:
        Slugified text with Unicode characters normalized to ASCII
    """
    # Normalize Unicode characters to their closest ASCII equivalents
    # This converts é -> e, ñ -> n, etc.
    text = unicodedata.normalize("NFKD", text)
    # Remove combining characters (diacritics) and keep only ASCII
    text = text.encode("ascii", "ignore").decode("ascii")
    # Convert to lowercase and strip whitespace
    text = text.lower().strip()
    # Remove any remaining non-word characters (keep only alphanumeric, underscore, hyphen)
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace whitespace and multiple hyphens with single hyphen
    text = re.sub(r"[-\s]+", "-", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    return text


class Command(BaseCommand):
    """Fix GameTag slugs that contain Unicode characters.

    This command regenerates slugs for all GameTag objects, ensuring
    they only contain ASCII characters that match the URL pattern.

    Usage:
        python manage.py fix_gametag_slugs [--dry-run]
    """

    help = "Fix GameTag slugs with Unicode characters"

    def add_arguments(self, parser):
        """Add command arguments.

        Args:
            parser: Argument parser instance.
        """
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed without actually updating",
        )

    def handle(self, *args, **options):
        """Execute the command.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.
        """
        dry_run = options["dry_run"]
        updated_count = 0
        unchanged_count = 0

        self.stdout.write("Checking GameTag slugs...")

        for gametag in GameTag.objects.all():
            # Generate new slug using ASCII normalization
            new_slug = slugify_ascii(gametag.name)

            # Check if slug needs updating
            if gametag.slug != new_slug:
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Would update: '{gametag.name}' "
                            f"(slug: '{gametag.slug}' -> '{new_slug}')"
                        ),
                    )
                else:
                    old_slug = gametag.slug
                    gametag.slug = new_slug
                    gametag.save(update_fields=["slug"])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updated: '{gametag.name}' "
                            f"(slug: '{old_slug}' -> '{new_slug}')"
                        ),
                    )
                updated_count += 1
            else:
                unchanged_count += 1

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nDry run complete. Would update {updated_count} slug(s), "
                    f"{unchanged_count} unchanged."
                ),
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nComplete! Updated {updated_count} slug(s), "
                    f"{unchanged_count} unchanged."
                ),
            )
