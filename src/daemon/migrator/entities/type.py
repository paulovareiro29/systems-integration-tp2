import uuid


class Type:
    def __init__(self, name):
        self._id = uuid.uuid5(uuid.NAMESPACE_OID, name)
        self._name = name

    def __str__(self):
        return f"({self._id}) {self._name}"
