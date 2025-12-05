from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Company(models.Model):
    """Company that produces sound products."""

    name = models.CharField(_("Name"), max_length=255, unique=True)
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """Get URL for company's detail view.

        Returns:
            str: URL for company detail.
        """
        return reverse("sources:company_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    """Product (hardware/software) produced by a company."""

    name = models.CharField(_("Name"), max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Company"),
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["company__name", "name"]
        unique_together = [["name", "company"]]

    def __str__(self) -> str:
        return f"{self.company.name} - {self.name}"

    def get_absolute_url(self) -> str:
        """Get URL for product's detail view.

        Returns:
            str: URL for product detail.
        """
        return reverse("sources:product_detail", kwargs={"pk": self.pk})


class Bank(models.Model):
    """Bank within a product."""

    name = models.CharField(_("Name"), max_length=255)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="banks",
        verbose_name=_("Product"),
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
        ordering = ["product__company__name", "product__name", "name"]
        unique_together = [["name", "product"]]

    def __str__(self) -> str:
        return f"{self.product} - {self.name}"

    def get_absolute_url(self) -> str:
        """Get URL for bank's detail view.

        Returns:
            str: URL for bank detail.
        """
        return reverse("sources:bank_detail", kwargs={"pk": self.pk})


class SoundSource(models.Model):
    """Sound source (sample, patch, etc.) from a bank or product."""

    name = models.CharField(_("Name"), max_length=255)
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="sound_sources",
        null=True,
        blank=True,
        verbose_name=_("Bank"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sound_sources",
        null=True,
        blank=True,
        verbose_name=_("Product"),
    )
    discoverers = models.ManyToManyField(
        User,
        related_name="discovered_sources",
        blank=True,
        verbose_name=_("Discoverers"),
    )
    games = models.ManyToManyField(
        "games.Game",
        related_name="sound_sources",
        blank=True,
        verbose_name=_("Games"),
    )
    songs = models.ManyToManyField(
        "songs.Song",
        related_name="sound_sources",
        blank=True,
        verbose_name=_("Songs"),
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Sound Source")
        verbose_name_plural = _("Sound Sources")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """Validate that at least one of bank or product is set.

        A sound source can have:
        - A product only (no bank)
        - Both a product and a bank (since banks are part of products)

        Raises:
            ValidationError: If neither bank nor product is set.
        """
        super().clean()
        if not self.bank and not self.product:
            raise ValidationError(
                _("Sound source must have either a bank OR a product.")
            )

    def save(self, *args, **kwargs) -> None:
        """Save the sound source after validation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for sound source's detail view.

        Returns:
            str: URL for sound source detail.
        """
        return reverse("sources:soundsource_detail", kwargs={"pk": self.pk})
