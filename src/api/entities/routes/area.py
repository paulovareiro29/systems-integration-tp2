from flask import Blueprint, jsonify, request
from utils.database import Database

from entities import Area

bpArea = Blueprint("area", __name__)


@bpArea.route("/", methods=["GET"])
def index():
    db = Database()
    result: list[Area] = []
    for area in db.selectAll("SELECT id, name, created_on, updated_on FROM areas"):
        result.append(Area(id=area[0],
                           name=area[1],
                           created_on=area[2],
                           updated_on=area[3]))

    return jsonify([area.__dict__ for area in result])


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
        result = db.delete(f"DELETE FROM areas WHERE id = %s", (id,))
        return jsonify(result), 200
    except Exception:
        return jsonify(), 400


@bpArea.route("/<id>", methods=["PUT"])
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
