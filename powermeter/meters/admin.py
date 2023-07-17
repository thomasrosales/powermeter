from django.contrib import admin

from .models import Measure, Instrument, Tag

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    
    list_display = ("name", "meter_key", "created")
    list_filter = ("name", "meter_key", "created")
    search_fields = ("name", "meter_key", "created")



@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ("consumption", "instrument", "created")
    list_filter = ("instrument", "created")
    search_fields = ("consumption", "instrument", "created")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created")
    list_filter = ("name", "created")
    search_fields = ("name", "created")