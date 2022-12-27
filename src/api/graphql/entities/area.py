import graphene


class Area(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    created_on = graphene.DateTime()
    updated_on = graphene.DateTime()
