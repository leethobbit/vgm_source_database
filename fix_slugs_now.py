#!/usr/bin/env python
"""Quick script to fix GameTag slugs with Unicode characters.

Run this immediately to fix broken slugs:
    python fix_slugs_now.py
"""

import os
import re
import sys
import unicodedata

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from vgm_source_database.games.models import GameTag


def slugify_ascii(text: str) -> str:
    """Convert text to slug, normalizing Unicode characters to ASCII."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    text = text.strip("-")
    return text


def main():
    """Fix all GameTag slugs."""
    print("Fixing GameTag slugs...")
    updated_count = 0

    for gametag in GameTag.objects.all():
        new_slug = slugify_ascii(gametag.name)

        if gametag.slug != new_slug:
            old_slug = gametag.slug
            gametag.slug = new_slug
            gametag.save(update_fields=["slug"])
            print(f"✓ Updated: '{gametag.name}' (slug: '{old_slug}' -> '{new_slug}')")
            updated_count += 1
        else:
            print(f"  OK: '{gametag.name}' (slug: '{gametag.slug}')")

    print(f"\nComplete! Updated {updated_count} slug(s).")


if __name__ == "__main__":
    main()
