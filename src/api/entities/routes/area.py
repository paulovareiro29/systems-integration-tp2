import math
from flask import Blueprint, jsonify, request
from utils.safe import toSafeInt
from utils.database import Database

from entities import Area

bpArea = Blueprint("area", __name__)


@bpArea.route("/", methods=["GET"])
def index():
    page = toSafeInt(request.args.get("page"), 0)
    limit = toSafeInt(request.args.get("limit"), 50)

    db = Database()
    result: list[Area] = []

    maxEntities = db.selectOne(f"SELECT count(id) FROM areas")
    for area in db.selectAll(f"SELECT id, name, created_on, updated_on FROM areas OFFSET {page * limit} LIMIT {limit}"):
        result.append(Area(id=area[0],
                           name=area[1],
                           created_on=area[2],
                           updated_on=area[3]))

    return jsonify({"data": [area.__dict__ for area in result],
                    "pagination": {"count": maxEntities[0],
                                   "last_page": math.ceil(maxEntities[0] / limit) - 1,
                                   "page": page,
                                   "limit": limit}})


@bpArea.route("/<id>", methods=["GET"])
def get(id):
    db = Database()
    result = db.selectOne(
        "SELECT id, name, created_on, updated_on FROM areas WHERE id=%s", (id,))

    if result is None:
        return jsonify(), 200

    area = Area(id=result[0],
                name=result[1],
                created_on=result[2],
                updated_on=result[3])
    return jsonify(area.__dict__), 200


@bpArea.route("/", methods=["POST"])
def create():
    data = request.get_json()

    try:
        area = Area(id=data.get("id"),
                    name=data["name"])

        db = Database()
        db.insert(
            "INSERT INTO areas (id, name, created_on, updated_on) VALUES (%s, %s, %s, %s)", (str(area.id), area.name, area.created_on, area.updated_on))
        return jsonify(area.__dict__), 201
    except Exception:
        return jsonify(), 400


@bpArea.route("/<id>", methods=["DELETE"])
def delete(id):
    try:
        db = Database()

        if db.selectOne(f"SELECT count(id) FROM airbnbs WHERE area_id = %s", (id,))[0] > 0:
            raise Exception("Integrity error")

        result = db.delete(f"DELETE FROM areas WHERE id = %s", (id,))
        return jsonify(result), 200
    except Exception:
        return jsonify(), 400


@ bpArea.route("/<id>", methods=["PUT"])
def update(id):
    data = request.get_json()

    area = Area(id=id, name=data["name"])

    try:
        db = Database()
        db.update(
            f"UPDATE areas SET name=%s, updated_on=%s WHERE id=%s", (area.name, area.updated_on, str(area.id)))

        return get(id)
    except Exception:
        return jsonify(), 400
