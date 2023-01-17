from django.db import models
from model_utils.models import TimeStampedModel


class Meter(TimeStampedModel):
    meter_key = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.meter_key}"


class Measure(TimeStampedModel):
    consumption = models.PositiveIntegerField()
    meter = models.ForeignKey(Meter, related_name="measures", on_delete=models.CASCADE)

    def __str__(self):
        return f"Measure's meter {self.meter_id} consumption: {self.consumption}"
