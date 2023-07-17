from django.db import models
from model_utils.models import TimeStampedModel


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class Instrument(TimeStampedModel):
    meter_key = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"instrument_{self.name}"


class Measure(TimeStampedModel):
    consumption = models.PositiveIntegerField(default=0)
    instrument = models.ForeignKey(Instrument, related_name="measures", on_delete=models.CASCADE)

    def __str__(self):
        return f"Measure's Instrument {self.instrument_id} consumption: {self.consumption}"


class Tag(TimeStampedModel):
    name = models.CharField(unique=True, max_length=200)
    instrument = models.ManyToManyField(Instrument, related_name="tags")

    def __str__(self):
        return f"{self.name}"
