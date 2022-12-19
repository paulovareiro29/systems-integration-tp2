import uuid

from utils.database import Database


class Airbnb:
    def __init__(self, id, name, price, host, type, area, neighbourhood, latitude, longitude):
        self._id = str(uuid.uuid5(uuid.NAMESPACE_OID, id))
        self._name = str(name)
        self._price = float(price) if price is not None else 0
        self._host = host
        self._type = type
        self._area = area
        self._neighbourhood = str(neighbourhood)
        self._latitude = float(latitude) if latitude is not None else 0
        self._longitude = float(longitude) if longitude is not None else 0

    def insertIntoDB(self):
        try:
            db = Database(host="db-rel")

            db.insert(
                f'''INSERT INTO airbnbs (id, name, price, host_id, type_id, area_id, neighbourhood, geom) VALUES (%s,%s,%s,%s,%s,%s,%s,'POINT(%s %s)')''', (self._id, self._name, self._price, self._host._id, self._type._id, self._area._id, self._neighbourhood, self._latitude, self._longitude))
            Airbnb.counter += 1
        except Exception as err:
            res = db.selectOne(
                f"SELECT id FROM airbnbs WHERE id = '{self._id}'")
            if res is not None:
                self._id = res[0]

    def __str__(self):
        return f"({self._id}) {self._name} {self._price} {self._latitude} {self._longitude}"


Airbnb.counter = 0
