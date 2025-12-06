"""Utilities for importing YAML fixtures with duplicate handling."""

import yaml
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction


def import_fixture_file(
    file_path: str,
    duplicate_handling: str = "skip",
    verbosity: int = 1,
) -> dict:
    """Import YAML fixture file with duplicate handling.

    Args:
        file_path: Path to YAML fixture file
        duplicate_handling: How to handle duplicates - "skip" or "overwrite"
        verbosity: Verbosity level (0=minimal, 1=normal, 2=verbose)

    Returns:
        Dictionary with import statistics:
        {
            "total": int,
            "created": int,
            "updated": int,
            "skipped": int,
            "errors": list
        }
    """
    stats = {
        "total": 0,
        "created": 0,
        "updated": 0,
        "skipped": 0,
        "errors": [],
    }

    # Load YAML file
    with open(file_path, "r", encoding="utf-8") as f:
        fixture_data = yaml.safe_load(f)

    if not fixture_data:
        return stats

    if not isinstance(fixture_data, list):
        raise ValueError("YAML file must contain a list of objects")

    stats["total"] = len(fixture_data)

    # Process each object
    for idx, item in enumerate(fixture_data, start=1):
        try:
            model_path = item["model"]
            app_label, model_name = model_path.split(".")
            model_class = apps.get_model(app_label, model_name)

            pk = item.get("pk")
            fields = item.get("fields", {})

            # Separate ManyToMany fields from regular fields
            many_to_many_fields = {}
            regular_fields = {}
            
            for field_name, value in fields.items():
                try:
                    field = model_class._meta.get_field(field_name)
                    if field.many_to_many:
                        many_to_many_fields[field_name] = value
                    else:
                        regular_fields[field_name] = value
                except Exception:
                    # Field might not exist, skip it
                    continue

            # Handle duplicates based on option
            if duplicate_handling == "overwrite":
                # Use update_or_create to overwrite existing objects
                obj, created = model_class.objects.update_or_create(
                    pk=pk,
                    defaults=regular_fields,
                )
                if created:
                    stats["created"] += 1
                else:
                    stats["updated"] += 1

                # Update ManyToMany relationships
                for field_name, value in many_to_many_fields.items():
                    if value:  # Only if not empty
                        getattr(obj, field_name).set(value)

            else:  # skip
                # Check if object with this PK already exists
                try:
                    existing_obj = model_class.objects.filter(pk=pk).first()
                    if existing_obj:
                        stats["skipped"] += 1
                        if verbosity >= 2:
                            print(f"Skipped duplicate: {model_path} pk={pk}")
                    else:
                        # Create new object
                        with transaction.atomic():
                            obj = model_class.objects.create(pk=pk, **regular_fields)
                            stats["created"] += 1
                            # Set ManyToMany fields for newly created objects
                            for field_name, value in many_to_many_fields.items():
                                if value:  # Only if not empty
                                    getattr(obj, field_name).set(value)
                except IntegrityError as e:
                    # Handle unique constraint violations (e.g., duplicate name)
                    stats["skipped"] += 1
                    # Extract more useful error information
                    error_str = str(e)
                    # Try to extract the constraint name or field name
                    if "unique constraint" in error_str.lower():
                        error_msg = f"Item {idx} ({model_path} pk={pk}): Unique constraint violation - {error_str}"
                    elif "foreign key" in error_str.lower():
                        error_msg = f"Item {idx} ({model_path} pk={pk}): Foreign key constraint violation - {error_str}"
                    elif "not-null constraint" in error_str.lower():
                        error_msg = f"Item {idx} ({model_path} pk={pk}): Not-null constraint violation - {error_str}"
                    else:
                        error_msg = f"Item {idx} ({model_path} pk={pk}): {error_str}"
                    stats["errors"].append(error_msg)
                    if verbosity >= 1:
                        print(f"Skipped duplicate: {model_path} pk={pk}")

        except Exception as e:
            stats["skipped"] += 1
            model_path = item.get("model", "unknown")
            pk = item.get("pk", "unknown")
            error_type = type(e).__name__
            error_msg = f"Item {idx} ({model_path} pk={pk}): [{error_type}] {str(e)}"
            stats["errors"].append(error_msg)
            if verbosity >= 1:
                print(f"Error processing {error_msg}")

    return stats
