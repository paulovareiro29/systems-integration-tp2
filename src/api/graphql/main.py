import sys

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS

from utils.database import Database

from entities.type import Type
from entities.area import Area
from entities.airbnb import Airbnb

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000


class Query(graphene.ObjectType):
    types = graphene.List(Type)
    areas = graphene.List(Area)
    airbnbs = graphene.List(Airbnb)

    by_area = graphene.List(Airbnb, name=graphene.String())
    by_type = graphene.List(Airbnb, name=graphene.String())
    by_higher_price = graphene.List(Airbnb, value=graphene.Int())
    by_lower_price = graphene.List(Airbnb, value=graphene.Int())

    def resolve_types(self, info):
        try:
            db = Database()
            result = []
            for type in db.selectAll("SELECT id, name, created_on, updated_on FROM types"):
                result.append(
                    Type(id=type[0], name=type[1], created_on=type[2], updated_on=type[3]))

            return result
        except:
            return []

    def resolve_areas(self, info):
        try:
            db = Database()
            result = []
            for area in db.selectAll("SELECT id, name, created_on, updated_on FROM areas"):
                result.append(
                    Area(id=area[0], name=area[1], created_on=area[2], updated_on=area[3]))

            return result
        except:
            return []

    def resolve_airbnbs(self, info):
        try:
            db = Database()
            result = []
            for airbnb in db.selectAll("SELECT id, name, price, created_on, updated_on FROM airbnbs"):
                result.append(
                    Airbnb(id=airbnb[0], name=airbnb[1], price=airbnb[2], created_on=airbnb[3], updated_on=airbnb[4]))

            return result
        except:
            return []

    def resolve_by_area(self, info, name):
        try:
            db = Database()
            result = []
            for airbnb in db.selectAll("SELECT airbnb.id, airbnb.name, airbnb.price, airbnb.created_on, airbnb.updated_on FROM airbnbs as airbnb, areas as area WHERE area.name = %s AND airbnb.area_id = area.id", (name,)):
                result.append(
                    Airbnb(id=airbnb[0], name=airbnb[1], price=airbnb[2], created_on=airbnb[3], updated_on=airbnb[4]))

            return result
        except Exception as err:
            return []

    def resolve_by_type(self, info, name):
        try:
            db = Database()
            result = []
            for airbnb in db.selectAll("SELECT airbnb.id, airbnb.name, airbnb.price, airbnb.created_on, airbnb.updated_on FROM airbnbs as airbnb, types as type WHERE type.name = %s AND airbnb.type_id = type.id", (name,)):
                result.append(
                    Airbnb(id=airbnb[0], name=airbnb[1], price=airbnb[2], created_on=airbnb[3], updated_on=airbnb[4]))

            return result
        except Exception as err:
            return []

    def resolve_by_higher_price(self, info, value):
        try:
            db = Database()
            result = []
            for airbnb in db.selectAll("SELECT id, name, price, created_on, updated_on FROM airbnbs WHERE price > %s", (value,)):
                result.append(
                    Airbnb(id=airbnb[0], name=airbnb[1], price=airbnb[2], created_on=airbnb[3], updated_on=airbnb[4]))

            return result
        except Exception as err:
            return []

    def resolve_by_lower_price(self, info, value):
        try:
            db = Database()
            result = []
            for airbnb in db.selectAll("SELECT id, name, price, created_on, updated_on FROM airbnbs WHERE price < %s", (value,)):
                result.append(
                    Airbnb(id=airbnb[0], name=airbnb[1], price=airbnb[2], created_on=airbnb[3], updated_on=airbnb[4]))

            return result
        except Exception as err:
            return []


schema = graphene.Schema(query=Query)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config["DEBUG"] = True

    CORS(app)

    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.run(host="0.0.0.0", port=PORT)
