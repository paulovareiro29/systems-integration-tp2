from utils.xml import XMLElement


class Airbnb:

    def __init__(self, id, name: str, host_id, host_name, host_verified, neighbourhood: str, price, area, type, latitude, longitude):
        self._id = id
        self._name = name
        self._host_id = host_id
        self._host_name = host_name
        self._host_verified = host_verified if host_verified != "" else "unconfirmed"
        self._price = str(price).replace("$", "").replace(",", "").strip()
        self._neighbourhood = neighbourhood
        self._area = area
        self._type = type
        self._latitude = latitude
        self._longitude = longitude

    def to_xml(self):
        airbnb = XMLElement(tag="Airbnb",
                            attrib={
                                "id": str(self._id),
                                "type_ref": str(self._type.get_id())
                            })
        airbnb.append(XMLElement(tag="Name", text=self._name))
        airbnb.append(XMLElement(tag="Price", text=self._price))

        host = XMLElement(tag="Host",
                          attrib={
                              "id": str(self._host_id)
                          })

        host.append(XMLElement(tag="Name", text=self._host_name))
        host.append(XMLElement(tag="Verified", text=self._host_verified))

        address = XMLElement(tag="Address",
                             attrib={
                                 "area_ref": str(self._area.get_id())
                             })
        address.append(XMLElement(tag="Neighbourhood",
                                  text=self._neighbourhood))

        coordinates = XMLElement(tag="Coordinates")
        coordinates.append(XMLElement(tag="Latitude",
                                      text=self._latitude))
        coordinates.append(XMLElement(tag="Longitude",
                                      text=self._longitude))

        address.append(coordinates)

        airbnb.append(host)
        airbnb.append(address)

        return airbnb

    def __str__(self):
        return f"{self._name} ({self._id})"
