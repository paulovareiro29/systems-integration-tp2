from utils.xml import XMLElement


class Area:

    def __init__(self, name):
        Area.counter += 1
        self._id = Area.counter
        self._name = name
        self._lat = 0
        self._lon = 0

    def to_xml(self):
        el = XMLElement(tag="Area", attrib={
            "id": str(self._id),
            "name": self._name,
            "lat": str(self._lat),
            "lon": str(self._lon)
        })
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"id:{self._id}, name: {self._name}, lat: {self._lat}, lon: {self._lon}"


Area.counter = 0
