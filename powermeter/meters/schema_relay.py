import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from .models import Measure, Instrument
from .schema import InstrumentType


# ES UNA SIMPLIFICACION Y PERMITE RESOLVER FILTRADO DE MODELOS
# DE MANERA SENCILLA Y TAMBIEN LAS MUTACIONES

class MeasureNode(DjangoObjectType):

    class Meta:
        model = Measure
        interfaces = relay.Node,
        filter_fields = {
            "consumption": ["exact"],
            "instrument__name": ["exact", 'icontains', 'istartswith'],
        }


class MeasureQuery(ObjectType):
    all_measures = DjangoFilterConnectionField(MeasureNode)
    measure = relay.Node.Field(MeasureNode)


# Mutation with Relay

class InstrumentUpdateRelayMutation(relay.ClientIDMutation):
    """

    Example::

        update_instrument_relay = InstrumentUpdateRelayMutation.Field()

        mutation MutateInstrumentRelay{
            updateInstrumentRelay(
                input: {id:"TWCASDASD", title: "TestNew"}
            ){
                instrument{
                    id
                    name
                    meter_key
                }
            }
        }

    """

    class Input:
        id = graphene.ID(required=True)
        name = graphene.String()
        meter_key = graphene.String()

    instrument = graphene.Field(InstrumentType)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id, name=None, meter_key=None):
        # through an error if it does not exist
        instrument = Instrument.objects.get(pk=from_global_id(id))
        if name:
            instrument.name = name
        if meter_key:
            instrument.meter_key = meter_key
        instrument.save()
        return InstrumentUpdateRelayMutation(instrument=instrument)
