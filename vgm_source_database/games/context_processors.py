from django.db.models import Count

from .models import GameTag


def top_categories(request):
    """Provide top game tags sorted by occurrence count.

    Returns:
        dict: Context dictionary with 'top_categories' key containing
              GameTag queryset annotated with game count, sorted by count descending.
    """
    top_categories = (
        GameTag.objects.annotate(game_count=Count("games"))
        .filter(game_count__gt=0)
        .order_by("-game_count")[:20]
    )
    return {"top_categories": top_categories}
