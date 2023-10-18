import graphene
from graphene import ObjectType, Mutation
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Instrument, Measure


class MeasureType(DjangoObjectType):

    class Meta:
        model = Measure


class InstrumentType(DjangoObjectType):
    measures = graphene.List(MeasureType)

    class Meta:
        model = Instrument

    instrument_age = graphene.String()  # Decorate calls with extra information in the ObjectType side

    def resolve_instrument_age(self, info, **kwargs):
        return "Old instrument" if self.created.year >= 2020 else "New Instrument"

    def resolve_measures(self, info, **kwargs):
        return self.measures.all()


class MetersQuery(ObjectType):
    all_instruments = graphene.List(InstrumentType)
    # all_measures = graphene.List(MeasureType)
    instrument = graphene.Field(InstrumentType, id=graphene.Int(), name=graphene.String())
    # FIXME: replaced by relay measure = graphene.Field(MeasureType, id=graphene.Int())  # single field with the same type. Accept parameters like ID

    @login_required
    def resolve_all_instruments(self, info, **kwargs):
        return Instrument.objects.all()

    # @login_required
    # def resolve_all_measures(self, info, **kwargs):
    #     return Measure.objects.all()

    # Single Instrument query

    @login_required
    def resolve_instrument(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id := kwargs.get("id"):
            return Instrument.objects.prefetch_related("measures").get(pk=id)

        if name := kwargs.get("name"):
            return Instrument.objects.prefetch_related("measures").get(name=name)

        return None

    # @login_required
    # def resolve_measure(self, info, **kwargs):
    #     id = kwargs.get("id")
    #
    #     if id := kwargs.get("id"):
    #         return Measure.objects.select_related("instrument").get(pk=id)
    #
    #     return None


class InstrumentCreateMutation(Mutation):

    class Arguments:
        name = graphene.String(required=True)
        meter_key = graphene.String(required=True)

    instrument = graphene.Field(InstrumentType)

    @login_required
    def mutate(self, info, name, meter_key, **kwargs):
        instrument = Instrument.objects.create(name=name, meter_key=meter_key)
        return InstrumentCreateMutation(instrument=instrument)


class InstrumentAddMeasureMutation(Mutation):

    class Arguments:
        id = graphene.ID(required=True)
        consumption = graphene.Int(required=True)

    instrument = graphene.Field(InstrumentType)

    @login_required
    def mutate(self, info, id, consumption, **kwargs):
        if consumption <= 0:
            raise Exception("Invalid")
        instrument = Instrument.objects.get(pk=id)
        measure = Measure(consumption=consumption, instrument=instrument)
        measure.save()
        return InstrumentAddMeasureMutation(instrument=instrument)


class InstrumentUpdateMutation(Mutation):

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        meter_key = graphene.String()

    instrument = graphene.Field(InstrumentType)

    @login_required
    def mutate(self, info, id, name=None, meter_key=None):
        # through an error if it does not exist
        instrument = Instrument.objects.get(pk=id)
        if name:
            instrument.name = name
        if meter_key:
            instrument.meter_key = meter_key
        instrument.save()
        return InstrumentUpdateMutation(instrument=instrument)


class InstrumentDeleteMutation(Mutation):

    class Arguments:
        id = graphene.ID(required=True)

    instrument = graphene.Field(InstrumentType)

    @login_required
    def mutate(self, info, id):
        # through an error if it does not exist
        instrument = Instrument.objects.get(pk=id)
        if instrument:
            instrument.delete()
        return InstrumentDeleteMutation(instrument=None)


class MetersMutation:
    create_instrument = InstrumentCreateMutation.Field()
    update_instrument = InstrumentUpdateMutation.Field()
    delete_instrument = InstrumentDeleteMutation.Field()
    add_measure = InstrumentAddMeasureMutation.Field()

