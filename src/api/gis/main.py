import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.database import Database

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

''' @app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args

    return [
        {
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [41.69462, -8.84679]
            },
            "properties": {
                "id": "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
                "name": "Ronaldo",
                "country": "Portugal",
                "position": "Striker",
                "imgUrl": "https://cdn-icons-png.flaticon.com/512/805/805401.png",
                "number": 7
            }
        }
    ] '''


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
                    FROM (SELECT id, name, geom FROM airbnbs WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s)) AS t(id, name, geom)""", (neLat, neLng, swLat, swLng))

        res = []
        for m in markers:
            res.append(m)

        return jsonify(res)
    except Exception as err:
        print(err)
        return jsonify(), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
