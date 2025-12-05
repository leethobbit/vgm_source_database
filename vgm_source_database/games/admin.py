from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Game, GameTag


@admin.register(GameTag)
class GameTagAdmin(admin.ModelAdmin):
    """Admin interface for GameTag model."""

    list_display = ["name", "slug", "created_at", "updated_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Admin interface for Game model."""

    list_display = ["title", "release_date", "release_year", "created_at", "updated_at"]
    list_filter = ["tags", "release_year", "created_at"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["album_artists", "tags"]
