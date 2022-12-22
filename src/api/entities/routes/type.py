import math
from flask import Blueprint, jsonify, request
from utils.safe import toSafeInt
from utils.database import Database

from entities import Type

bpType = Blueprint("type", __name__)


@bpType.route("/", methods=["GET"])
def index():
    page = toSafeInt(request.args.get("page"), 0)
    limit = toSafeInt(request.args.get("limit"), 50)

    db = Database()
    result: list[Type] = []
    maxEntities = db.selectOne(f"SELECT count(id) FROM types")
    for type in db.selectAll(f"SELECT id, name, created_on, updated_on FROM types OFFSET {page * limit} LIMIT {limit}"):
        result.append(Type(id=type[0],
                           name=type[1],
                           created_on=type[2],
                           updated_on=type[3]))

    return jsonify({"data": [type.__dict__ for type in result],
                    "pagination": {"count": maxEntities[0],
                                   "last_page": math.ceil(maxEntities[0] / limit) - 1,
                                   "page": page,
                                   "limit": limit}})


@bpType.route("/<id>", methods=["GET"])
def get(id):
    db = Database()
    result = db.selectOne(
        "SELECT id, name, created_on, updated_on FROM types WHERE id=%s", (id,))

    if result is None:
        return jsonify(), 200

    type = Type(id=result[0],
                name=result[1],
                created_on=result[2],
                updated_on=result[3])
    return jsonify(type.__dict__), 200


@bpType.route("/", methods=["POST"])
def create():
    data = request.get_json()

    try:
        type = Type(id=data.get("id"),
                    name=data["name"])

        db = Database()
        db.insert(
            "INSERT INTO types (id, name, created_on, updated_on) VALUES (%s, %s, %s, %s)", (str(type.id), type.name, type.created_on, type.updated_on))
        return jsonify(type.__dict__), 201
    except Exception:
        return jsonify(), 400


@bpType.route("/<id>", methods=["DELETE"])
def delete(id):
    try:
        db = Database()

        if db.selectOne(f"SELECT count(id) FROM airbnbs WHERE type_id = %s", (id,))[0] > 0:
            raise Exception("Integrity error")

        result = db.delete(f"DELETE FROM types WHERE id = %s", (id,))
        return jsonify(result), 200
    except Exception:
        return jsonify(), 400


@bpType.route("/<id>", methods=["PUT"])
def update(id):
    data = request.get_json()

    type = Type(id=id, name=data["name"])

    try:
        db = Database()
        db.update(
            f"UPDATE types SET name=%s, updated_on=%s WHERE id=%s", (type.name, type.updated_on, str(type.id)))

        return get(id)
    except Exception:
        return jsonify(), 400
