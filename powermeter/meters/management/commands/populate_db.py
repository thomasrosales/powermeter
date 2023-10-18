from typing import Dict
from random import randint
from datetime import datetime

from faker import Faker
from django.core.management.base import BaseCommand

from powermeter.meters.models import Instrument, Measure, Tag


class Command(BaseCommand):
    INSTRUMENT_LIMIT = 25
    HISTORIC_INSTRUMENT_LIMIT = 25
    MEASURE_LIMIT = 250
    TAG_LIMIT = 250

    faker = Faker()
    help = "This command is used to populate the database with dummy data"

    def _create_instruments(self) -> Dict[str, set]:
        dataset = {
            "name": set(),
            "meter_key": set(),
        }

        for _ in range(self.INSTRUMENT_LIMIT+1):
            dataset["name"].add(self.faker.word())

        names_dataset_length = len(dataset["name"])

        for _ in range(names_dataset_length):
            dataset["meter_key"].add(self.faker.uuid4())

        self.stdout.write(self.style.SUCCESS(f"Created {names_dataset_length} MOCK Instruments"))
        return dataset

    # faker.date_time_between(datetime(year=2020,month=1,day=1), datetime(year=2023,month=12,day=28))
    def _create_historic_instruments(self) -> Dict[str, set]:
        dataset = {
            "name": set(),
            "meter_key": set(),
            "dates": set(),
        }

        for index, _ in enumerate (range(self.INSTRUMENT_LIMIT+1)):
            dataset["name"].add(f"{self.faker.word()}-historic_{index}")

        names_dataset_length = len(dataset["name"])

        for _ in range(names_dataset_length):
            dataset["meter_key"].add(self.faker.uuid4())

        for _ in range(names_dataset_length):
            dataset["dates"].add(self.faker.date_time_between(datetime(year=2020,month=1,day=1), datetime(year=2023,month=12,day=28)))

        self.stdout.write(self.style.SUCCESS(f"Created {names_dataset_length} MOCK Instruments"))
        return dataset

    def _create_measure_objects(self) -> Dict[str, list]:
        dataset = {
            "consumption": [],
            "instrument": [],
            "date": []
        }
        for _ in range(self.MEASURE_LIMIT):
            dataset["consumption"].append(self.faker.pyint())
            dataset["instrument"].append(self.faker.random_int(min=1, max=self.INSTRUMENT_LIMIT))
            dataset["date"].append(self.faker.date_time_between(datetime(year=2020,month=1,day=1), datetime(year=2023,month=12,day=28)))

        self.stdout.write(self.style.SUCCESS(f"Created {self.MEASURE_LIMIT} MOCK Measure objects"))

        return dataset

    def _create_tags(self) -> Dict[str, set]:
        dataset = set()

        for _ in range(self.TAG_LIMIT):
            dataset.add(self.faker.word())

        self.stdout.write(self.style.SUCCESS(f"Created {len(dataset)} MOCK Tags"))
        return dataset

    def handle(self, *args, **options):
        common_list = []
        instruments_dataset = self._create_instruments()
        measures_dataset = self._create_measure_objects()
        tags_dataset = self._create_tags()
        instrumets_historic_dataset = self._create_historic_instruments()

        self.stdout.write(self.style.NOTICE("Populating database..."))
        self.stdout.write(self.style.NOTICE("Populating Instruments Model..."))

        for name, meter_key in zip(instruments_dataset["name"], instruments_dataset["meter_key"]):
            common_list.append(Instrument(name=name, meter_key=meter_key))

        Instrument.objects.bulk_create(common_list)
        self.stdout.write(self.style.SUCCESS("Successfully populated Instruments Model"))

        # they are just 25 instruments, so we can afford to do this...
        instrument_queryset = Instrument.objects.all()
        instruments_map = {instrument.id : instrument for instrument in instrument_queryset}

        self.stdout.write(self.style.NOTICE("Populating Measure Model..."))
        common_list = []
        for consumption, instrument, date in zip(measures_dataset["consumption"], measures_dataset["instrument"], measures_dataset["date"]):
            common_list.append(Measure(consumption=consumption, instrument_id=instruments_map[instrument].id, created=date))

        Measure.objects.bulk_create(common_list)
        self.stdout.write(self.style.SUCCESS("Successfully populated Measure Model"))

        self.stdout.write(self.style.NOTICE("Populating Tag Model..."))
        common_list = []
        for name in tags_dataset:
            common_list.append(Tag(name=name))

        Tag.objects.bulk_create(common_list)
        self.stdout.write(self.style.SUCCESS("Successfully populated Tag Model"))

        tags = Tag.objects.all()
        self.stdout.write(self.style.NOTICE("Linking random tags with the random Instrument Model..."))
        for tag in tags:
            _instrument = instrument_queryset[randint(1, self.INSTRUMENT_LIMIT)]
            tag.instrument.add(_instrument)
            tag.save()


        self.stdout.write(self.style.NOTICE("Populating Historic Instrument Model..."))
        common_list = []
        for name, meter_key, date in zip(instrumets_historic_dataset["name"], instrumets_historic_dataset["meter_key"], instrumets_historic_dataset["dates"]):
            common_list.append(Instrument(name=name, meter_key=meter_key, created=date))

        Instrument.objects.bulk_create(common_list)
        self.stdout.write(self.style.SUCCESS("Successfully populated Historic Instrument Model"))

        self.stdout.write(self.style.SUCCESS("Successfully populated database"))




