import uuid
from datetime import datetime


class Airbnb:
    def __init__(self, name,  host_id, geom=None, latitude=None, longitude=None, price=0, neighbourhood=None, street=None, type_id=None, area_id=None, id=None, created_on=None, updated_on=None):
        self.id = id or uuid.uuid4()
        self.name = name
        self.price = price
        self.host_id = host_id
        self.type_id = type_id
        self.area_id = area_id
        self.neighbourhood = neighbourhood
        self.geom = geom if geom is not None else f"POINT({latitude} {longitude})" if latitude is not None and longitude is not None else None
        self.street = street
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()
