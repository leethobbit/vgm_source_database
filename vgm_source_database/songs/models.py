from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    """Person (composer, arranger, sound team member, etc.)."""

    name = models.CharField(_("Name"), max_length=255)
    products = models.ManyToManyField(
        "sources.Product",
        related_name="users",
        blank=True,
        verbose_name=_("Products"),
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """Get URL for person's detail view.

        Returns:
            str: URL for person detail.
        """
        return reverse("songs:person_detail", kwargs={"pk": self.pk})


class Song(models.Model):
    """Song from a game."""

    title = models.CharField(_("Title"), max_length=255)
    game = models.ForeignKey(
        "games.Game",
        on_delete=models.CASCADE,
        related_name="songs",
        verbose_name=_("Game"),
    )
    composers = models.ManyToManyField(
        Person,
        related_name="composed_songs",
        blank=True,
        verbose_name=_("Composers"),
    )
    arrangers = models.ManyToManyField(
        Person,
        related_name="arranged_songs",
        blank=True,
        verbose_name=_("Arrangers"),
    )
    track_number = models.PositiveIntegerField(_("Track Number"), null=True, blank=True)
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")
        ordering = ["game__title", "track_number", "title"]
        unique_together = [["title", "game"]]

    def __str__(self) -> str:
        return f"{self.game.title} - {self.title}"

    def get_absolute_url(self) -> str:
        """Get URL for song's detail view.

        Returns:
            str: URL for song detail.
        """
        return reverse("songs:song_detail", kwargs={"pk": self.pk})
