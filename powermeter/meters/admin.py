from django.contrib import admin

from .models import Measure, Instrument


@admin.register(Instrument)
class MeterAdmin(admin.ModelAdmin):
    pass


@admin.register(Measure)
class MeterAdmin(admin.ModelAdmin):
    pass
