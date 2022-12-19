import sys

import graphene
from flask import Flask
from flask_graphql import GraphQLView

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.Argument(graphene.String, default_value="World"))

    def resolve_hello(self, info, name):
        return f'Hello {name}!'


schema = graphene.Schema(query=Query)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.run(host="0.0.0.0", port=PORT)
