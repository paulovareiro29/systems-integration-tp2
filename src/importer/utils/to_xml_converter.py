import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from utils.reader import CSVReader

from entities.type import Type
from entities.area import Area
from entities.airbnb import Airbnb


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):

        # read areas
        areas = self._reader.read_entities(
            attr="neighbourhood group",
            builder=lambda row: Area(row["neighbourhood group"])
        )

        # read types
        types = self._reader.read_entities(
            attr="room type",
            builder=lambda row: Type(row["room type"])
        )

        # read airbnb
        airbnbs = self._reader.read_entities(
            attr="id",
            builder=lambda row: Airbnb(
                id=row["id"],
                name=row["NAME"],
                host_id=row["host id"],
                host_name=row["host name"],
                host_verified=row["host_identity_verified"],
                neighbourhood=row["neighbourhood"],
                price=row["price"],
                latitude=row["lat"],
                longitude=row["long"],
                area=areas[row["neighbourhood group"]],
                type=types[row["room type"]]
            )
        )

        # generate the final xml
        root_el = ET.Element("Root")

        areas_el = ET.Element("Areas")
        for area in areas.values():
            areas_el.append(area.to_xml())

        types_el = ET.Element("Types")
        for type in types.values():
            types_el.append(type.to_xml())

        airbnbs_el = ET.Element("Airbnbs")
        for airbnb in airbnbs.values():
            airbnbs_el.append(airbnb.to_xml())

        root_el.append(areas_el)
        root_el.append(types_el)
        root_el.append(airbnbs_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(
            self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()
