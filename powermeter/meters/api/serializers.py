from rest_framework import serializers

from ..models import Measure, Meter


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
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
            "meter",
            "created",
            "modified",
        )
        read_only_fields = (
            "id",
            "created",
            "modified",
        )
