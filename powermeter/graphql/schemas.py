from graphene import ObjectType, Schema

from powermeter.meters.schema import MetersQuery, MetersMutation
from powermeter.meters.schema_relay import MeasureQuery

from .jwt import JWTMutation



# Si hay mas schemas se separar por como y se agregan como herencia
class Query(MeasureQuery, MetersQuery, ObjectType):
    pass


class Mutation(JWTMutation, MetersMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
