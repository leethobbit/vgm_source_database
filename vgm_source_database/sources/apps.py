from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SourcesConfig(AppConfig):
    name = "vgm_source_database.sources"
    verbose_name = _("Sources")
