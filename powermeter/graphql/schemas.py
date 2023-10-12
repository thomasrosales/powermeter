from graphene import ObjectType, Schema

from powermeter.meters import schema as meters_schema


# Si hay mas schemas se separar por como y se agregan como herencia
class Query(meters_schema.Query, ObjectType):
    pass


class Mutation(meters_schema.Mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
