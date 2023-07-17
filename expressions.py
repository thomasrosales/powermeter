from django.db.models import F,Q
from datetime import datetime

# Q

# Ejmplo: AND - OR - NOT

## Medidas que no sean del 20220
Measure.objects.filter(
    Q(created__gte=datetime(2023, 1, 1))
    | Q(created__lt=datetime(2022, 1,1)) 
) 


# PROBAR: .values_list("created__year").distinct()

## NOR

Measure.objects.filter(~Q(created__year=2022))

## AND

Measure.objects.filter(
    Q(created__gte=datetime(2020, 1, 1))
    & ~Q(instrument__name__startswith="m") 
) 

# BUENAS PRACTICAS

measure_after_2023 = Q(created__gte=datetime(2023, 1, 1))
measure_before_2022 = Q(created__lt=datetime(2022, 1,1))

Measure.objects.filter(measure_after_2023 | measure_before_2022)

# F - Agrupamiento

count_instruments_by_measures  = (   
    Measure.objects
    .values("instrument_id")
    .annotate(total_measures=Count("id"))
)

instruments_with_more_than_100_measures = (
    Measure.objects
    .values("instrument_id")
    .annotate(total_measures=Count("id"))
    .filter(total_measures__gt=10)
)

tags_by_instruments = (
    Instrument.objects
    .values("tags__name")
    .annotate(total_tags=Count("id"))
)

instruments_avg_consumption = (
    Measure.objects
    .values("instrument_id")
    .annotate(consumption=Avg("consumption"))
)


# Calcular impuestos por consumo por instrumento
instruments = (
    Measure.objects
    .filter(created__year=2023)
    .annotate(taxes=F("consumption") * 5.5)
    .values("instrument_id")
    .annotate(total=Sum("taxes"))
    .values_list("id", "total")
    .order_by("total")
)