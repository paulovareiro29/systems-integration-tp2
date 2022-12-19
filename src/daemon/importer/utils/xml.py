
import xml.etree.ElementTree as ET


def XMLElement(tag, attrib=None, text=None):
    if attrib:
        element = ET.Element(tag, attrib)
    else:
        element = ET.Element(tag)
    element.text = text
    return element
