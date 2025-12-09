"""Utilities for importing YAML fixtures with duplicate handling."""

import yaml
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import ForeignKey


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

            # Separate ManyToMany fields from regular fields and resolve ForeignKeys
            many_to_many_fields = {}
            regular_fields = {}
            
            for field_name, value in fields.items():
                try:
                    field = model_class._meta.get_field(field_name)
                    
                    # Handle ManyToMany fields
                    if field.many_to_many:
                        many_to_many_fields[field_name] = value
                    # Handle ForeignKey fields - check for related_model attribute (more reliable than isinstance)
                    elif hasattr(field, 'related_model') and field.related_model is not None:
                        # Resolve ForeignKey: look up the related model instance
                        if value is None:
                            # Allow null foreign keys
                            regular_fields[field_name] = None
                        else:
                            # Get the related model and look up the instance
                            related_model = field.related_model
                            try:
                                related_instance = related_model.objects.get(pk=value)
                                regular_fields[field_name] = related_instance
                            except related_model.DoesNotExist:
                                # Related object doesn't exist - this will cause an error
                                # but we'll let Django handle it with a proper error message
                                regular_fields[field_name] = value
                            except Exception as e:
                                # If there's an error looking up the instance, keep the original value
                                # Django will provide a better error message
                                if verbosity >= 2:
                                    print(f"Warning: Could not resolve {field_name}={value} for {model_path}: {e}")
                                regular_fields[field_name] = value
                    else:
                        # Regular field (CharField, TextField, IntegerField, etc.)
                        regular_fields[field_name] = value
                except Exception as e:
                    # Field might not exist or there's an error accessing it
                    # Log it but don't fail the entire import
                    if verbosity >= 2:
                        print(f"Warning: Skipping field {field_name} for {model_path}: {e}")
                    # Still add it as a regular field in case it's a custom field or something
                    regular_fields[field_name] = value

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
                        # Resolve primary keys to instances
                        field = model_class._meta.get_field(field_name)
                        related_model = field.related_model
                        instances = related_model.objects.filter(pk__in=value)
                        getattr(obj, field_name).set(instances)

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
                                    # Resolve primary keys to instances
                                    field = model_class._meta.get_field(field_name)
                                    related_model = field.related_model
                                    instances = related_model.objects.filter(pk__in=value)
                                    getattr(obj, field_name).set(instances)
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
