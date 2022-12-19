import sys
import time
import signal

from utils.database import Database

from entities.area import Area
from entities.type import Type
from entities.host import Host
from entities.airbnb import Airbnb

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def handler(signum, frame):
    print("\nExiting..")
    exit(1)


signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":

    # Connect to both databases
    db_org = None
    db_dst = None

    while True:
        try:
            db_org = Database(host="db-xml")
            db_dst = Database(host="db-rel")
            print("Connected to databases!")
            break
        except Exception as err:
            print(err)
            time.sleep(POLLING_FREQ)

    while True:
        if db_dst is None or db_org is None:
            break

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        doc = db_org.selectOne(
            "SELECT id FROM imported_documents WHERE migrated IS false AND deleted_on IS NULL")

        if doc is None:
            time.sleep(POLLING_FREQ)
            continue

        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        areas = []
        types = []
        hosts = []
        airbnbs = []

        for area in db_org.selectAll(
                f"SELECT unnest(xpath('//Area/@id', area)) AS id, unnest(xpath('//Area/@name', area)) FROM (SELECT unnest(xpath('//Areas/Area', xml)) AS area FROM imported_documents WHERE id = {doc[0]}) t"):
            areas.append((area[0], Area(name=area[0])))

        for type in db_org.selectAll(
                f"SELECT unnest(xpath('//Type/@id', type)) AS id, unnest(xpath('//Type/@name', type)) FROM (SELECT unnest(xpath('//Types/Type', xml)) AS type FROM imported_documents WHERE id = {doc[0]}) t"):
            types.append((type[0], Type(name=type[1])))

        for host in db_org.selectAll(
                f"SELECT unnest(xpath('//Airbnb/Host/@id', airbnb)) AS id, unnest(xpath('//Airbnb/Host/Name/text()', airbnb)) AS name, unnest(xpath('//Airbnb/Host/Verified/text()', airbnb)) AS status  FROM (SELECT unnest(xpath('//Airbnbs/Airbnb', xml)) AS airbnb FROM imported_documents WHERE id = {doc[0]}) s"):
            hosts.append(
                (host[0], Host(id=host[0], name=host[1], status=host[2])))

        for airbnb in db_org.selectAll(
                f"SELECT unnest(xpath('//Airbnb/@id', airbnb)) AS id, unnest(xpath('//Airbnb/Name/text()', airbnb)) AS name,  unnest(xpath('//Airbnb/Price/text()', airbnb)) AS price, unnest(xpath('//Airbnb/Host/@id', airbnb)) AS host, unnest(xpath('//Airbnb/Address/@area_ref', airbnb)) AS area, unnest(xpath('//Airbnb/@type_ref', airbnb)) AS type, unnest(xpath('//Airbnb/Address/Neighbourhood/text()', airbnb)) AS neighbourhood,  unnest(xpath('//Airbnb/Address/Coordinates/Latitude/text()', airbnb)) AS latitude, unnest(xpath('//Airbnb/Address/Coordinates/Longitude/text()', airbnb)) AS Longitude  FROM (SELECT unnest(xpath('//Airbnbs/Airbnb', xml)) AS airbnb FROM imported_documents WHERE id = {doc[0]}) s"):

            area = list(filter(lambda x: x[0] == airbnb[4], areas))
            if len(area) <= 0:
                print("Area not found.. Skipping airbnb")
                continue

            type = list(filter(lambda x: x[0] == airbnb[5], types))
            if len(type) <= 0:
                print("Type not found.. Skipping airbnb")
                continue

            host = list(filter(lambda x: x[0] == airbnb[3], hosts))
            if len(host) <= 0:
                print("Host not found.. Skipping airbnb")
                continue

            airbnbs.append(Airbnb(id=airbnb[0],
                                  name=airbnb[1],
                                  price=airbnb[2],
                                  host=host[0][1],
                                  type=type[0][1],
                                  area=area[0][1],
                                  neighbourhood=airbnb[6],
                                  latitude=airbnb[7],
                                  longitude=airbnb[8]))
        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        time.sleep(POLLING_FREQ)