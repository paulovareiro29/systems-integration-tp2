import uuid


class Host:
    def __init__(self, id, name, status):
        self._id = uuid.uuid5(uuid.NAMESPACE_OID, id)
        self._name = name
        self._status = status

    def __str__(self):
        return f" ({self._id}) {self._name} - {self._status}"
