from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Bank, Company, Product, SoundSource


class CompanyListView(ListView):
    """List view for companies."""

    model = Company
    context_object_name = "companies"
    template_name = "sources/company_list.html"


class CompanyDetailView(DetailView):
    """Detail view for a company."""

    model = Company
    context_object_name = "company"
    template_name = "sources/company_detail.html"


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """Create view for companies."""

    model = Company
    fields = ["name", "notes"]
    template_name = "sources/company_form.html"


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for companies."""

    model = Company
    fields = ["name", "notes"]
    template_name = "sources/company_form.html"


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for companies."""

    model = Company
    template_name = "sources/company_confirm_delete.html"
    success_url = reverse_lazy("sources:company_list")


class ProductListView(ListView):
    """List view for products."""

    model = Product
    context_object_name = "products"
    template_name = "sources/product_list.html"


class ProductDetailView(DetailView):
    """Detail view for a product."""

    model = Product
    context_object_name = "product"
    template_name = "sources/product_detail.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Create view for products."""

    model = Product
    fields = ["name", "company", "notes"]
    template_name = "sources/product_form.html"


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for products."""

    model = Product
    fields = ["name", "company", "notes"]
    template_name = "sources/product_form.html"


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for products."""

    model = Product
    template_name = "sources/product_confirm_delete.html"
    success_url = reverse_lazy("sources:product_list")


class BankListView(ListView):
    """List view for banks."""

    model = Bank
    context_object_name = "banks"
    template_name = "sources/bank_list.html"


class BankDetailView(DetailView):
    """Detail view for a bank."""

    model = Bank
    context_object_name = "bank"
    template_name = "sources/bank_detail.html"


class BankCreateView(LoginRequiredMixin, CreateView):
    """Create view for banks."""

    model = Bank
    fields = ["name", "product", "notes"]
    template_name = "sources/bank_form.html"


class BankUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for banks."""

    model = Bank
    fields = ["name", "product", "notes"]
    template_name = "sources/bank_form.html"


class BankDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for banks."""

    model = Bank
    template_name = "sources/bank_confirm_delete.html"
    success_url = reverse_lazy("sources:bank_list")


class SoundSourceListView(ListView):
    """List view for sound sources."""

    model = SoundSource
    context_object_name = "sound_sources"
    template_name = "sources/soundsource_list.html"


class SoundSourceDetailView(DetailView):
    """Detail view for a sound source."""

    model = SoundSource
    context_object_name = "sound_source"
    template_name = "sources/soundsource_detail.html"


class SoundSourceCreateView(LoginRequiredMixin, CreateView):
    """Create view for sound sources."""

    model = SoundSource
    fields = ["name", "bank", "product", "discoverers", "games", "songs", "notes"]
    template_name = "sources/soundsource_form.html"


class SoundSourceUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for sound sources."""

    model = SoundSource
    fields = ["name", "bank", "product", "discoverers", "games", "songs", "notes"]
    template_name = "sources/soundsource_form.html"


class SoundSourceDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for sound sources."""

    model = SoundSource
    template_name = "sources/soundsource_confirm_delete.html"
    success_url = reverse_lazy("sources:soundsource_list")
