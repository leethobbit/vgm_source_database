import os
import tempfile

import yaml

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.management import call_command
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, View

from .forms import ImportDataForm
from .import_utils import import_fixture_file
from .games.models import Game, GameTag
from .songs.models import Person, Song
from .sources.models import Bank, Company, Product, SoundSource


class HomeView(TemplateView):
    """Dashboard homepage view with stats and recent activity."""

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        """Get context data for the dashboard.

        Returns:
            dict: Context data including stats and recent activity.
        """
        context = super().get_context_data(**kwargs)

        # Stats
        context["stats"] = {
            "companies": Company.objects.count(),
            "products": Product.objects.count(),
            "sound_sources": SoundSource.objects.count(),
            "games": Game.objects.count(),
            "songs": Song.objects.count(),
            "people": Person.objects.count(),
        }

        # Recent activity (last 15 CRUD operations)
        recent_limit = 15
        context["recent_activity"] = []
        # Track URLs of objects already added as "Created" to avoid duplicates
        created_urls = set()

        # Helper function to add activity items
        def add_activity_items(queryset, model_name, get_name_func, get_url_func):
            """Add create and update activities for a queryset.

            Args:
                queryset: QuerySet to process
                model_name: Name of the model type
                get_name_func: Function to get display name from object
                get_url_func: Function to get URL from object
            """
            # Get recent creates
            for obj in queryset.order_by("-created_at")[:recent_limit]:
                url = get_url_func(obj)
                context["recent_activity"].append(
                    {
                        "action": "Created",
                        "type": model_name,
                        "name": get_name_func(obj),
                        "url": url,
                        "timestamp": obj.created_at,
                    }
                )
                # Track this URL to exclude from updates
                created_urls.add(url)

            # Get recent updates (only if updated_at != created_at)
            # Exclude objects that were already added as "Created"
            for obj in queryset.filter(
                updated_at__gt=F("created_at")
            ).order_by("-updated_at")[:recent_limit]:
                url = get_url_func(obj)
                # Skip if this object was already added as "Created"
                if url not in created_urls:
                    context["recent_activity"].append(
                        {
                            "action": "Updated",
                            "type": model_name,
                            "name": get_name_func(obj),
                            "url": url,
                            "timestamp": obj.updated_at,
                        }
                    )

        # Track activities for all models
        add_activity_items(
            Company.objects.all(),
            "Company",
            lambda obj: obj.name,
            lambda obj: obj.get_absolute_url(),
        )
        add_activity_items(
            Product.objects.all(),
            "Product",
            lambda obj: str(obj),
            lambda obj: obj.get_absolute_url(),
        )
        add_activity_items(
            Bank.objects.all(),
            "Bank",
            lambda obj: str(obj),
            lambda obj: obj.get_absolute_url(),
        )
        add_activity_items(
            SoundSource.objects.all(),
            "Sound Source",
            lambda obj: obj.name,
            lambda obj: obj.get_absolute_url(),
        )
        add_activity_items(
            Game.objects.all(),
            "Game",
            lambda obj: obj.title,
            lambda obj: obj.get_absolute_url(),
        )
        add_activity_items(
            GameTag.objects.all(),
            "Game Tag",
            lambda obj: obj.name,
            lambda obj: obj.get_absolute_url(),
        )
        add_activity_items(
            Song.objects.all(),
            "Song",
            lambda obj: f"{obj.game.title} - {obj.title}",
            lambda obj: obj.get_absolute_url(),
        )
        add_activity_items(
            Person.objects.all(),
            "Person",
            lambda obj: obj.name,
            lambda obj: obj.get_absolute_url(),
        )

        # Sort by timestamp descending and limit to recent_limit
        context["recent_activity"].sort(key=lambda x: x["timestamp"], reverse=True)
        context["recent_activity"] = context["recent_activity"][:recent_limit]

        return context


class ImportDataView(LoginRequiredMixin, FormView):
    """View for importing YAML fixture files.

    Allows authenticated users to upload and import YAML fixture files.
    """

    form_class = ImportDataForm
    template_name = "pages/import_data.html"
    success_url = reverse_lazy("data:import_data")

    def form_valid(self, form):
        """Handle valid form submission.

        Args:
            form: Valid ImportDataForm instance

        Returns:
            HttpResponse: Redirect response
        """
        fixture_file = form.cleaned_data["fixture_file"]
        dry_run = form.cleaned_data["dry_run"]
        duplicate_handling = form.cleaned_data.get("duplicate_handling", "skip")

        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode="wb") as tmp_file:
            for chunk in fixture_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        try:
            # Run import command
            if dry_run:
                # For dry-run, validate YAML structure and Django fixture format
                try:
                    with open(tmp_file_path, "r", encoding="utf-8") as f:
                        yaml_data = yaml.safe_load(f)
                        if not yaml_data:
                            raise ValueError("YAML file is empty or invalid")
                        if not isinstance(yaml_data, list):
                            raise ValueError("YAML file must contain a list of objects")
                        
                        # Validate Django fixture format
                        for idx, item in enumerate(yaml_data, start=1):
                            if not isinstance(item, dict):
                                raise ValueError(f"Item {idx} is not a dictionary")
                            
                            # Check required keys
                            if "model" not in item:
                                raise ValueError(f"Item {idx} is missing 'model' key")
                            if "pk" not in item:
                                raise ValueError(f"Item {idx} is missing 'pk' key")
                            if "fields" not in item:
                                raise ValueError(f"Item {idx} is missing 'fields' key")
                            
                            # Validate model format (should be app_label.ModelName with exactly 2 parts)
                            model = item["model"]
                            if not isinstance(model, str):
                                raise ValueError(f"Item {idx} has invalid 'model' type (must be string)")
                            
                            model_parts = model.split(".")
                            if len(model_parts) != 2:
                                raise ValueError(
                                    f"Item {idx} has invalid model format '{model}'. "
                                    f"Expected 'app_label.ModelName' (2 parts), got {len(model_parts)} parts."
                                )
                            
                            # Validate fields is a dictionary
                            if not isinstance(item["fields"], dict):
                                raise ValueError(f"Item {idx} has invalid 'fields' type (must be dictionary)")
                        
                        # Count objects
                        object_count = len(yaml_data)
                        messages.success(
                            self.request,
                            f"Validation successful! File '{fixture_file.name}' contains {object_count} object(s) and is ready to import. "
                            "Uncheck 'Dry Run' to perform the actual import.",
                        )
                except yaml.YAMLError as yaml_error:
                    messages.error(
                        self.request,
                        f"YAML parsing error: {str(yaml_error)}",
                    )
                except Exception as validation_error:
                    messages.error(
                        self.request,
                        f"Validation failed: {str(validation_error)}",
                    )
            else:
                # Actual import using custom handler with duplicate handling
                stats = import_fixture_file(
                    tmp_file_path,
                    duplicate_handling=duplicate_handling,
                    verbosity=0,
                )
                
                # Build success message with statistics
                msg_parts = [
                    f"Import complete! Processed {stats['total']} object(s).",
                    f"Created: {stats['created']}",
                    f"Updated: {stats['updated']}" if duplicate_handling == "overwrite" else f"Skipped: {stats['skipped']}",
                ]
                
                if stats["errors"]:
                    msg_parts.append(f"Errors: {len(stats['errors'])}")
                    # Store errors in session for detailed viewing
                    self.request.session["import_errors"] = stats["errors"][:1000]  # Limit to first 1000 errors
                    self.request.session["import_error_count"] = len(stats["errors"])
                    messages.warning(
                        self.request,
                        " | ".join(msg_parts) + f" <a href='#errors' class='underline'>View error details</a>.",
                        extra_tags="safe",
                    )
                else:
                    messages.success(
                        self.request,
                        " | ".join(msg_parts),
                    )
        except Exception as e:
            messages.error(
                self.request,
                f"Error importing file: {str(e)}",
            )
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add import errors to context if they exist.

        Args:
            **kwargs: Variable keyword arguments.

        Returns:
            dict: Context dictionary.
        """
        context = super().get_context_data(**kwargs)
        # Errors are already in session, template can access them directly
        return context


class ClearImportErrorsView(LoginRequiredMixin, View):
    """Clear import errors from session."""

    def post(self, request, *args, **kwargs):
        """Clear import errors from session.

        Args:
            request: HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Redirect response.
        """
        if "import_errors" in request.session:
            del request.session["import_errors"]
        if "import_error_count" in request.session:
            del request.session["import_error_count"]
        return redirect("data:import_data")
