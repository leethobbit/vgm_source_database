from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Person, Song


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin interface for Person model."""

    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["products"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """Admin interface for Song model."""

    list_display = ["title", "game", "track_number", "created_at", "updated_at"]
    list_filter = ["game", "created_at"]
    search_fields = ["title", "game__title"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["game"]
    filter_horizontal = ["composers", "arrangers"]
