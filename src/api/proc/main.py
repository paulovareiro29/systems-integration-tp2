import sys

from flask import Flask, request
from xmlrpc.client import ServerProxy

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/airbnbs', methods=['GET'])
def fetch_airbnbs():
    server = ServerProxy("http://rpc-server:9000")

    try:
        return server.fetchAirbnbs()
    except Exception as e:
        print(e)
        return []


@app.route('/api/areas', methods=['GET'])
def fetch_areas():
    server = ServerProxy("http://rpc-server:9000")

    try:
        return server.fetchAreas()
    except Exception as e:
        print(e)
        return []


@app.route('/api/types', methods=['GET'])
def fetch_types():
    server = ServerProxy("http://rpc-server:9000")

    try:
        return server.fetchTypes()
    except Exception as e:
        print(e)
        return []


@app.route('/api/count/airbnbs', methods=['GET'])
def count_airbnbs():
    server = ServerProxy("http://rpc-server:9000")

    try:
        return server.countAirbnbs()
    except Exception as e:
        print(e)
        return []


@app.route('/api/airbnbs/area', methods=['GET'])
def fetch_by_areas():
    server = ServerProxy("http://rpc-server:9000")
    args = request.args

    try:
        name = args["name"]
        return server.fetchByArea(name)
    except Exception as e:
        print(e)
        return []


@app.route('/api/airbnbs/type', methods=['GET'])
def fetch_by_types():
    server = ServerProxy("http://rpc-server:9000")
    args = request.args

    try:
        name = args["name"]
        return server.fetchByType(name)
    except Exception as e:
        print(e)
        return []


@app.route('/api/airbnbs/price/higher', methods=['GET'])
def fetch_by_higher_price():
    server = ServerProxy("http://rpc-server:9000")
    args = request.args

    try:
        value = args["value"]
        return server.fetchByPriceHigherThen(value)
    except Exception as e:
        print(e)
        return []


@app.route('/api/airbnbs/price/lower', methods=['GET'])
def fetch_by_lower_price():
    server = ServerProxy("http://rpc-server:9000")
    args = request.args

    try:
        value = args["value"]
        return server.fetchByPriceLowerThen(value)
    except Exception as e:
        print(e)
        return []


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
