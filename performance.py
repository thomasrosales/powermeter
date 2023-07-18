# Performance


# N+1 QUERY

instruments = Instrument.objects.all()[:2]

for instrument in instruments:
    print(instrument.tags.all())

# NOTA: realiza 1 query por cada instrumento para obtener los tags
# carga en memoria

# SOLUTION

## MANY_TO_ONE or MANY_TO_MANY

Instrument.objects.prefetch_related("tags", "measures").all()[:2]

## ONE_TO_MANY

Measure.objects.select_related("instrument").all()[:2]

# Mistake 1: Busacar usando el ORM
# Las medidas de los instrumentos que empiezan con M

for measure in Measure.objects.all()[:2]:
    if measure.instrument.name.startswith("m"):
        print(f"Encontre: {measure.id}")

# Soluction 1
# Filtra el ORM directamente

for m in Measure.objects.filter(instrument__name__startswith="m"):
    print(f"Encontre {m.id}")        

# Solution: 2
# Filtro y obtengo la informacion que necesito

for m_id in Measure.objects.filter(instrument__name__startswith="m").values_list("id", flat=True):
    print(f"Encontre: {m_id}")


## Mistake 2: verificar si un objeto existe

try:
    instrument = Instrument.objects.get(id=999)
except Instrument.DoesNotExist as e:
    print(e)

instrument = Instrument.objects.filter(id=999)
if len(instrument) == 0:
    print("no existe")

## Soluition 1

if Instrument.objects.filter(id=999).exists():
    # existe


## Mistake 3: si necesitas el objeto completo, lo podes acceder directamente de la Foreing Key

measure = Measure.objects.get(id=1)

instrument_id = measure.instrument.id

## Note: 2 queries

## Solution

instrument_id = measure.instrument_id

## Nota 1 query












