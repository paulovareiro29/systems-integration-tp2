from utils.xml import XMLElement


class Area:

    def __init__(self, name):
        Area.counter += 1
        self._id = Area.counter
        self._name = name

    def to_xml(self):
        el = XMLElement(tag="Area", attrib={
            "id": str(self._id),
            "name": self._name
        })
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"id:{self._id}, name: {self._name}"


Area.counter = 0
