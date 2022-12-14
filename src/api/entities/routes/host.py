import math
from flask import Blueprint, jsonify, request
from utils.safe import toSafeInt
from utils.database import Database

from entities import Host

bpHost = Blueprint("host", __name__)


@bpHost.route("/", methods=["GET"])
def index():
    page = toSafeInt(request.args.get("page"), 0)
    limit = toSafeInt(request.args.get("limit"), 50)

    db = Database()
    result: list[Host] = []
    maxEntities = db.selectOne(f"SELECT count(id) FROM hosts")
    for host in db.selectAll(f"SELECT id, name,verified, created_on, updated_on FROM hosts OFFSET {page * limit} LIMIT {limit}"):
        result.append(Host(id=host[0],
                           name=host[1],
                           verified=host[2],
                           created_on=host[3],
                           updated_on=host[4]))

    return jsonify({"data": [host.__dict__ for host in result],
                    "pagination": {"count": maxEntities[0],
                                   "last_page": math.ceil(maxEntities[0] / limit) - 1,
                                   "page": page,
                                   "limit": limit}})


@bpHost.route("/<id>", methods=["GET"])
def get(id):
    db = Database()
    result = db.selectOne(
        "SELECT id, name, verified, created_on, updated_on FROM hosts WHERE id=%s", (id,))

    if result is None:
        return jsonify(), 200

    host = Host(id=result[0],
                name=result[1],
                verified=result[2],
                created_on=result[3],
                updated_on=result[4])
    return jsonify(host.__dict__), 200


@bpHost.route("/", methods=["POST"])
def create():
    data = request.get_json()

    try:
        host = Host(id=data.get("id"),
                    name=data["name"],
                    verified=data.get("verified"))

        db = Database()
        db.insert(
            "INSERT INTO hosts (id, name, verified, created_on, updated_on) VALUES (%s, %s, %s, %s, %s)", (str(host.id), host.name, host.verified, host.created_on, host.updated_on))
        return jsonify(host.__dict__), 201
    except Exception:
        return jsonify(), 400


@bpHost.route("/<id>", methods=["DELETE"])
def delete(id):
    try:
        db = Database()

        if db.selectOne(f"SELECT count(id) FROM airbnbs WHERE host_id = %s", (id,))[0] > 0:
            raise Exception("Integrity error")

        result = db.delete(f"DELETE FROM hosts WHERE id = %s", (id,))
        return jsonify(result), 200
    except Exception:
        return jsonify(), 400


@bpHost.route("/<id>", methods=["PUT"])
def update(id):
    data = request.get_json()

    try:
        host = Host(id=id, name=data["name"], verified=data["verified"])

        db = Database()
        db.update(
            f"UPDATE hosts SET name=%s, verified=%s, updated_on=%s WHERE id=%s", (host.name, host.verified, host.updated_on, str(host.id)))

        return get(id)
    except Exception:
        return jsonify(), 400
