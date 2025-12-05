from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Bank, Company, Product, SoundSource


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model."""

    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""

    list_display = ["name", "company", "created_at", "updated_at"]
    list_filter = ["company", "created_at"]
    search_fields = ["name", "company__name"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["company"]


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    """Admin interface for Bank model."""

    list_display = ["name", "product", "created_at", "updated_at"]
    list_filter = ["product__company", "product", "created_at"]
    search_fields = ["name", "product__name", "product__company__name"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["product"]


@admin.register(SoundSource)
class SoundSourceAdmin(admin.ModelAdmin):
    """Admin interface for SoundSource model."""

    list_display = ["name", "bank", "product", "created_at", "updated_at"]
    list_filter = [
        "created_at",
        ("bank__product__company", admin.RelatedOnlyFieldListFilter),
        ("product__company", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["bank", "product"]
    filter_horizontal = ["discoverers", "games", "songs"]
