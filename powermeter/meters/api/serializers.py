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

    def validate_consumption(self, value):
        if value < 0:
            raise serializers.ValidationError("This field must contain a positive integer.")
        return value
