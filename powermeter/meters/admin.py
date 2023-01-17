from django.contrib import admin

from .models import Measure, Meter


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    pass


@admin.register(Measure)
class MeterAdmin(admin.ModelAdmin):
    pass
