from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Game, GameTag


class GameTagListView(ListView):
    """List view for game tags."""

    model = GameTag
    context_object_name = "game_tags"
    template_name = "games/gametag_list.html"


class GameTagDetailView(DetailView):
    """Detail view for a game tag."""

    model = GameTag
    context_object_name = "game_tag"
    slug_url_kwarg = "slug"
    template_name = "games/gametag_detail.html"


class GameTagCreateView(LoginRequiredMixin, CreateView):
    """Create view for game tags."""

    model = GameTag
    fields = ["name", "description"]
    template_name = "games/gametag_form.html"


class GameTagUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for game tags."""

    model = GameTag
    fields = ["name", "description"]
    template_name = "games/gametag_form.html"
    slug_url_kwarg = "slug"


class GameTagDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for game tags."""

    model = GameTag
    template_name = "games/gametag_confirm_delete.html"
    success_url = reverse_lazy("games:gametag_list")
    slug_url_kwarg = "slug"


class GameListView(ListView):
    """List view for games."""

    model = Game
    context_object_name = "games"
    template_name = "games/game_list.html"


class GameDetailView(DetailView):
    """Detail view for a game."""

    model = Game
    context_object_name = "game"
    template_name = "games/game_detail.html"

    def get_queryset(self):
        """Get queryset with optimized prefetching for songs and sound sources.

        Returns:
            QuerySet: Game queryset with prefetched songs and their sound sources.
        """
        return Game.objects.prefetch_related(
            "songs__sound_sources",
            "tags",
            "album_artists",
        )


class GameCreateView(LoginRequiredMixin, CreateView):
    """Create view for games."""

    model = Game
    fields = ["title", "release_date", "release_year", "album_artists", "tags", "notes"]
    template_name = "games/game_form.html"


class GameUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for games."""

    model = Game
    fields = ["title", "release_date", "release_year", "album_artists", "tags", "notes"]
    template_name = "games/game_form.html"


class GameDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for games."""

    model = Game
    template_name = "games/game_confirm_delete.html"
    success_url = reverse_lazy("games:game_list")
