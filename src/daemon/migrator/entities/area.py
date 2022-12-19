import uuid
from utils.database import Database


class Area:
    def __init__(self, name):
        self._id = uuid.uuid5(uuid.NAMESPACE_OID, name)
        self._name = str(name)

    def insertIntoDB(self):
        try:
            db = Database(host="db-rel")

            db.insert(f"INSERT INTO areas (name) VALUES ('{self._name}')")
        except Exception as err:
            res = db.selectOne(
                f"SELECT id FROM areas WHERE name = '{self._name}'")
            if res is not None:
                self._id = res[0]

    def __str__(self):
        return f"({self._id}) {self._name}"
