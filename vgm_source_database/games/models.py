from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class GameTag(models.Model):
    """Tag for categorizing games."""

    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Game Tag")
        verbose_name_plural = _("Game Tags")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        """Save the game tag, auto-generating slug if not provided.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for game tag's detail view.

        Returns:
            str: URL for game tag detail.
        """
        return reverse("games:gametag_detail", kwargs={"slug": self.slug})


class Game(models.Model):
    """Video game."""

    title = models.CharField(_("Title"), max_length=255)
    release_date = models.DateField(_("Release Date"), null=True, blank=True)
    release_year = models.IntegerField(_("Release Year"), null=True, blank=True)
    album_artists = models.ManyToManyField(
        "songs.Person",
        related_name="album_credits",
        blank=True,
        verbose_name=_("Album Artists"),
    )
    tags = models.ManyToManyField(
        GameTag,
        related_name="games",
        blank=True,
        verbose_name=_("Tags"),
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        """Get URL for game's detail view.

        Returns:
            str: URL for game detail.
        """
        return reverse("games:game_detail", kwargs={"pk": self.pk})
