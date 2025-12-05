from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SongsConfig(AppConfig):
    name = "vgm_source_database.songs"
    verbose_name = _("Songs")
