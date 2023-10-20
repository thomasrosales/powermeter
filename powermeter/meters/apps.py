from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MeterConfig(AppConfig):
    name = "powermeter.meters"
    verbose_name = _("Meters")

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import singals
