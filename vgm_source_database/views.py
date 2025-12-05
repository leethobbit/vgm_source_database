from django.db.models import F
from django.views.generic import TemplateView

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
