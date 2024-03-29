from django.db.models import Sum, Avg
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Measure, Instrument
from .serializers import MeasureSerializer, InstrumentSerializer


class InstrumentViewSet(ModelViewSet):
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()
    lookup_field = "meter_key"

    @action(detail=True, methods=["post"], serializer_class=MeasureSerializer)
    def add_measure(self, request, meter_key=None):
        instrument = self.get_object()
        serializer = self.get_serializer(data={**request.data, "instrument": instrument.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Measure added"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], serializer_class=MeasureSerializer)
    def max_consumption(self, request, meter_key=None):
        measure = (
            Measure.objects.filter(instrument__meter_key=meter_key)
            .order_by("-consumption")
            .first()
        )
        serializer = self.get_serializer(measure)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], serializer_class=MeasureSerializer)
    def min_consumption(self, request, meter_key=None):
        measure = (
            Measure.objects.filter(instrument__meter_key=meter_key)
            .order_by("consumption")
            .first()
        )
        serializer = self.get_serializer(measure)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def total_consumption(self, request, meter_key=None):
        total_consumption = (
            Measure.objects.filter(instrument__meter_key=meter_key)
            .aggregate(total=Sum("consumption"))
        )
        return Response({"status": {"total_consumption": total_consumption["total"]}}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def avg_consumption(self, request, meter_key=None):
        total_consumption = (
            Measure.objects.filter(instrument__meter_key=meter_key)
            .aggregate(total=Avg("consumption"))
        )
        return Response({"status": {"average_consumption": total_consumption["total"]}}, status=status.HTTP_200_OK)

