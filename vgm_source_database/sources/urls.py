from django.urls import path

from .views import (
    BankCreateView,
    BankDeleteView,
    BankDetailView,
    BankListView,
    BankUpdateView,
    CompanyCreateView,
    CompanyDeleteView,
    CompanyDetailView,
    CompanyListView,
    CompanyUpdateView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    SoundSourceCreateView,
    SoundSourceDeleteView,
    SoundSourceDetailView,
    SoundSourceListView,
    SoundSourceUpdateView,
)

app_name = "sources"
urlpatterns = [
    # Companies
    path("companies/", CompanyListView.as_view(), name="company_list"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company_detail"),
    path("companies/create/", CompanyCreateView.as_view(), name="company_create"),
    path("companies/<int:pk>/update/", CompanyUpdateView.as_view(), name="company_update"),
    path("companies/<int:pk>/delete/", CompanyDeleteView.as_view(), name="company_delete"),
    # Products
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    # Banks
    path("banks/", BankListView.as_view(), name="bank_list"),
    path("banks/<int:pk>/", BankDetailView.as_view(), name="bank_detail"),
    path("banks/create/", BankCreateView.as_view(), name="bank_create"),
    path("banks/<int:pk>/update/", BankUpdateView.as_view(), name="bank_update"),
    path("banks/<int:pk>/delete/", BankDeleteView.as_view(), name="bank_delete"),
    # Sound Sources
    path("", SoundSourceListView.as_view(), name="soundsource_list"),
    path("soundsources/<int:pk>/", SoundSourceDetailView.as_view(), name="soundsource_detail"),
    path("soundsources/create/", SoundSourceCreateView.as_view(), name="soundsource_create"),
    path("soundsources/<int:pk>/update/", SoundSourceUpdateView.as_view(), name="soundsource_update"),
    path("soundsources/<int:pk>/delete/", SoundSourceDeleteView.as_view(), name="soundsource_delete"),
]
