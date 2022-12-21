from flask import Blueprint, jsonify, request
from utils.database import Database

from entities import Airbnb

bpAirbnb = Blueprint("airbnb", __name__)


@bpAirbnb.route("/", methods=["GET"])
def index():
    page = int(request.args.get("page")) or 0
    perPage = int(request.args.get("perPage")) or 50

    db = Database()
    result: list[Airbnb] = []
    for airbnb in db.selectAll(f"SELECT id, name, price, host_id, type_id, area_id, neighbourhood, ST_X(geom), ST_Y(geom), geom, created_on, updated_on FROM airbnbs OFFSET {page * perPage} LIMIT {perPage}"):
        result.append(Airbnb(id=airbnb[0],
                             name=airbnb[1],
                             price=airbnb[2],
                             host_id=airbnb[3],
                             type_id=airbnb[4],
                             area_id=airbnb[5],
                             neighbourhood=airbnb[6],
                             latitude=airbnb[7],
                             longitude=airbnb[8],
                             geom=airbnb[9],
                             created_on=airbnb[10],
                             updated_on=airbnb[11]))

    return jsonify([airbnb.__dict__ for airbnb in result])


@bpAirbnb.route("/<id>", methods=["GET"])
def get(id):
    db = Database()
    result = db.selectOne(
        "SELECT id, name, price, host_id, type_id, area_id, neighbourhood, ST_X(geom), ST_Y(geom), geom, created_on, updated_on FROM airbnbs WHERE id=%s", (id,))

    if result is None:
        return jsonify(), 200

    airbnb = Airbnb(id=result[0],
                    name=result[1],
                    price=result[2],
                    host_id=result[3],
                    type_id=result[4],
                    area_id=result[5],
                    neighbourhood=result[6],
                    latitude=result[7],
                    longitude=result[8],
                    geom=result[9],
                    created_on=result[10],
                    updated_on=result[11])

    return jsonify(airbnb.__dict__), 200


@bpAirbnb.route("/", methods=["POST"])
def create():
    data = request.get_json()

    try:
        airbnb = Airbnb(id=data.get("id"),
                        name=data["name"],
                        price=data.get("price"),
                        host_id=data["host_id"],
                        type_id=data.get("type_id"),
                        area_id=data.get("area_id"),
                        neighbourhood=data.get("neighbourhood"),
                        latitude=data.get("latitude"),
                        longitude=data.get("longitude"))

        db = Database()
        db.insert(
            "INSERT INTO airbnbs (id, name, price, host_id, type_id, area_id, neighbourhood, geom, created_on, updated_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (str(airbnb.id), airbnb.name, airbnb.price, airbnb.host_id, airbnb.type_id, airbnb.area_id, airbnb.neighbourhood, airbnb.geom, airbnb.created_on, airbnb.updated_on))
        return jsonify(airbnb.__dict__), 201
    except Exception as err:
        print(err)
        return jsonify(), 400


@bpAirbnb.route("/<id>", methods=["DELETE"])
def delete(id):
    try:
        db = Database()
        result = db.delete(f"DELETE FROM airbnbs WHERE id = %s", (id,))
        return jsonify(result), 200
    except Exception:
        return jsonify(), 400


@bpAirbnb.route("/<id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    try:
        airbnb = Airbnb(id=id,
                        name=data["name"],
                        price=data.get("price"),
                        host_id=data["host_id"],
                        type_id=data.get("type_id"),
                        area_id=data.get("area_id"),
                        neighbourhood=data.get("neighbourhood"),
                        latitude=data.get("latitude"),
                        longitude=data.get("longitude"))

        db = Database()
        db.update(
            f"UPDATE airbnbs SET name=%s, price=%s, host_id=%s, type_id=%s, area_id=%s, neighbourhood=%s, geom=%s, updated_on=%s WHERE id=%s", (airbnb.name, airbnb.price, airbnb.host_id, airbnb.type_id, airbnb.area_id, airbnb.neighbourhood, airbnb.geom, airbnb.updated_on, id))

        return get(id)
    except Exception as err:
        print(err)
        return jsonify(), 400
