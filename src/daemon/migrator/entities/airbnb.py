import uuid


class Airbnb:
    def __init__(self, id, name, price, host, type, area, neighbourhood, latitude, longitude):
        self._id = uuid.uuid5(uuid.NAMESPACE_OID, id)
        self._name = name
        self._price = price
        self._host = host
        self._type = type
        self._area = area
        self._neighbourhood = neighbourhood
        self._latitude = latitude
        self._longitude = longitude

    def __str__(self):
        return f"({self._id}) {self._name} {self._price} {self._latitude} {self._longitude}"
