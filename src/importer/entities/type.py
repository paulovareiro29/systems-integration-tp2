from utils.xml import XMLElement


class Type:

    def __init__(self, name):
        Type.counter += 1
        self._id = Type.counter
        self._name = name

    def to_xml(self):
        el = XMLElement(tag="Type", attrib={
            "id": str(self._id),
            "name": self._name,
        })
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"id:{self._id}, name: {self._name}"


Type.counter = 0
