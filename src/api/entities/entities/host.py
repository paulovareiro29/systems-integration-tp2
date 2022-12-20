import uuid
from datetime import datetime


class Host:
    def __init__(self, name, verified="unconfirmed", id=None, created_on=None, updated_on=None):
        self.id = id or uuid.uuid4()
        self.name = name
        self.verified = verified
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()
