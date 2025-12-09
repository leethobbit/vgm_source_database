from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Person, Song


class PersonListView(ListView):
    """List view for people."""

    model = Person
    context_object_name = "people"
    template_name = "songs/person_list.html"
    paginate_by = 15

    def get_queryset(self):
        """Get queryset filtered by search query if provided.

        Returns:
            QuerySet: Filtered Person queryset.
        """
        queryset = super().get_queryset()
        search = self.request.GET.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) | models.Q(notes__icontains=search)
            )
        return queryset


class PersonDetailView(DetailView):
    """Detail view for a person."""

    model = Person
    context_object_name = "person"
    template_name = "songs/person_detail.html"


class PersonCreateView(LoginRequiredMixin, CreateView):
    """Create view for people."""

    model = Person
    fields = ["name", "products", "notes"]
    template_name = "songs/person_form.html"


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for people."""

    model = Person
    fields = ["name", "products", "notes"]
    template_name = "songs/person_form.html"


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for people."""

    model = Person
    template_name = "songs/person_confirm_delete.html"
    success_url = reverse_lazy("songs:person_list")


class SongListView(ListView):
    """List view for songs."""

    model = Song
    context_object_name = "songs"
    template_name = "songs/song_list.html"
    paginate_by = 15

    def get_queryset(self):
        """Get queryset filtered by search query if provided.

        Returns:
            QuerySet: Filtered Song queryset with prefetched game and composers.
        """
        queryset = super().get_queryset().select_related("game").prefetch_related("composers")
        search = self.request.GET.get("search", "").strip()
        if search:
            # Try to convert search to integer for track number search
            try:
                search_track = int(search)
                queryset = queryset.filter(
                    models.Q(title__icontains=search)
                    | models.Q(game__title__icontains=search)
                    | models.Q(track_number=search_track)
                    | models.Q(composers__name__icontains=search)
                ).distinct()
            except ValueError:
                # If search is not a number, don't search by track number
                queryset = queryset.filter(
                    models.Q(title__icontains=search)
                    | models.Q(game__title__icontains=search)
                    | models.Q(composers__name__icontains=search)
                ).distinct()
        return queryset


class SongDetailView(DetailView):
    """Detail view for a song."""

    model = Song
    context_object_name = "song"
    template_name = "songs/song_detail.html"


class SongCreateView(LoginRequiredMixin, CreateView):
    """Create view for songs."""

    model = Song
    fields = ["title", "game", "composers", "arrangers", "track_number", "notes"]
    template_name = "songs/song_form.html"


class SongUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for songs."""

    model = Song
    fields = ["title", "game", "composers", "arrangers", "track_number", "notes"]
    template_name = "songs/song_form.html"


class SongDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for songs."""

    model = Song
    template_name = "songs/song_confirm_delete.html"
    success_url = reverse_lazy("songs:song_list")
