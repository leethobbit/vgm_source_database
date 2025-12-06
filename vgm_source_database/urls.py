"""URL configuration for VGM Source Database main app."""

from django.urls import path

from .views import ClearImportErrorsView, ImportDataView

app_name = "data"

urlpatterns = [
    path("", ImportDataView.as_view(), name="import_data"),
    path("clear-errors/", ClearImportErrorsView.as_view(), name="clear_errors"),
]
