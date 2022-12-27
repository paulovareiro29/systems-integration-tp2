import graphene


class Airbnb(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    price = graphene.Int()
    created_on = graphene.DateTime()
    updated_on = graphene.DateTime()
