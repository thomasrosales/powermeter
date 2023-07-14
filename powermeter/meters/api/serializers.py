from rest_framework import serializers

from ..models import Measure, Instrument


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = (
            "id",
            "meter_key",
            "name",
            "created",
            "modified",
        )
        read_only_fields = (
            "id",
            "created",
            "modified",
        )


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = (
            "id",
            "consumption",
            "instrument",
            "created",
            "modified",
        )
        read_only_fields = (
            "id",
            "created",
            "modified",
        )
