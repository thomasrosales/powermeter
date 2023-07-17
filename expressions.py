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

# F

# Agrupamiento

