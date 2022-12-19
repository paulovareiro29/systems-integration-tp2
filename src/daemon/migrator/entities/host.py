import uuid

from utils.database import Database


class Host:
    def __init__(self, id, name, verified):
        self._id = uuid.uuid5(uuid.NAMESPACE_OID, id)
        self._name = name
        self._verified = verified

    def insertIntoDB(self):
        try:
            db = Database(host="db-rel")

            db.insert(
                f"INSERT INTO hosts (id, name, verified) VALUES ('{self._id}', '{self._name}', '{self._verified}')")
        except Exception as err:
            res = db.selectOne(
                f"SELECT id FROM hosts WHERE id = '{self._id}'")
            if res is not None:
                self._id = res[0]

    def __str__(self):
        return f" ({self._id}) {self._name} - {self._status}"
