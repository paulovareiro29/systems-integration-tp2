import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.database import Database

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)


@app.route('/api/tile')
def get_markers():
    args = request.args

    try:
        neLat = args["neLat"]
        neLng = args["neLng"]
        swLat = args["swLat"]
        swLng = args["swLng"]
    except:
        return jsonify("Invalid arguments"), 400

    try:
        db = Database()

        markers = db.selectAll(
            """SELECT jsonb_build_object(
                    'type', 'Feature',
                    'id', id,
                    'geometry', ST_AsGeoJSON(geom):: jsonb,
                    'properties', to_jsonb(t.*) - 'id' - 'geom'
                ) AS json
                    FROM (SELECT id, name, price, neighbourhood, street, geom FROM airbnbs WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s) AND street IS NOT NULL)  AS t(id, name, price, neighbourhood, street, geom)""", (neLat, neLng, swLat, swLng))

        res = []
        for m in markers:
            res.append(m[0])

        return jsonify(res)
    except Exception as err:
        print(err)
        return jsonify(), 400


@app.route('/api/airbnb', methods=["GET"])
def get_airbnbs():
    args = request.args

    limit = args.get("limit") or 20

    try:
        db = Database()

        result = []
        for airbnb in db.selectAll(f"SELECT id, name, price, host_id, type_id, area_id, neighbourhood, street, ST_X(geom), ST_Y(geom), geom, created_on, updated_on FROM airbnbs WHERE street IS NULL LIMIT %s", (limit,)):
            result.append({"id": airbnb[0],
                           "name": airbnb[1],
                           "price": airbnb[2],
                           "host_id": airbnb[3],
                           "type_id": airbnb[4],
                           "area_id": airbnb[5],
                           "neighbourhood": airbnb[6],
                           "street": airbnb[7],
                           "latitude": airbnb[8],
                           "longitude": airbnb[9],
                           "created_on": airbnb[11],
                           "updated_on": airbnb[12]})

        return jsonify(result)
    except Exception as err:
        print(err)
        return jsonify(), 400


@app.route("/api/airbnb/<id>", methods=["PUT"])
def update_airbnb(id):
    data = request.get_json()
    print("Updating..")
    try:
        street = data["street"]

        db = Database()
        db.update(f"UPDATE airbnbs SET street=%s WHERE id = %s", (street, id))

        return jsonify(True), 200
    except Exception as err:
        print(err)
        return jsonify(), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
