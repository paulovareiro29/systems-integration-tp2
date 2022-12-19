import sys
import time
import signal
import psycopg2.extras

from utils.database import Database

from entities.area import Area
from entities.type import Type
from entities.host import Host
from entities.airbnb import Airbnb

# Register UUID to be able to insert UUIDs
psycopg2.extras.register_uuid()

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
        doc = db_org.selectOne(
            "SELECT id FROM imported_documents WHERE migrated IS false AND deleted_on IS NULL")

        if doc is None:
            print("No updates found")
            print("Sleeping..\n")
            time.sleep(POLLING_FREQ)
            continue

        print("New document found!")

        Area.counter = 0
        Type.counter = 0
        Host.counter = 0
        Airbnb.counter = 0

        areas = []
        types = []
        hosts = []

        # Fetch areas from doc
        print(" - Processing areas..")
        for area in db_org.selectAll(
                f"SELECT unnest(xpath('//Area/@id', area)) AS id, unnest(xpath('//Area/@name', area)) FROM (SELECT unnest(xpath('//Areas/Area', xml)) AS area FROM imported_documents WHERE id = {doc[0]}) t"):
            element = Area(name=area[1])
            element.insertIntoDB()
            areas.append((area[0], element))

        print(f"   - Added {Area.counter} new areas")
        # Fetch types from doc
        print(" - Processing types..")
        for type in db_org.selectAll(
                f"SELECT unnest(xpath('//Type/@id', type)) AS id, unnest(xpath('//Type/@name', type)) FROM (SELECT unnest(xpath('//Types/Type', xml)) AS type FROM imported_documents WHERE id = {doc[0]}) t"):
            element = Type(name=type[1])
            element.insertIntoDB()
            types.append((type[0], element))

        print(f"   - Added {Type.counter} new types")

        # Fetch hosts from doc
        print(" - Processing hosts..")
        for host in db_org.selectAll(
                f"SELECT unnest(xpath('//Airbnb/Host/@id', airbnb)) AS id, unnest(xpath('//Airbnb/Host/Name/text()', airbnb)) AS name, unnest(xpath('//Airbnb/Host/Verified/text()', airbnb)) AS verified  FROM (SELECT unnest(xpath('//Airbnbs/Airbnb', xml)) AS airbnb FROM imported_documents WHERE id = {doc[0]}) s"):
            element = Host(id=host[0], name=host[1], verified=host[2])
            element.insertIntoDB()
            hosts.append(
                (host[0], element))

        print(f"   - Added {Host.counter} new hosts")

        # Fetch airbnbs from doc
        print(" - Processing airbnbs..")
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

            element = Airbnb(id=airbnb[0],
                             name=airbnb[1],
                             price=airbnb[2],
                             host=host[0][1],
                             type=type[0][1],
                             area=area[0][1],
                             neighbourhood=airbnb[6],
                             latitude=airbnb[7],
                             longitude=airbnb[8])

            element.insertIntoDB()

        print(f"   - Added {Airbnb.counter} new airbnbs")

        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.
        db_org.update(
            f"UPDATE imported_documents SET migrated = 'TRUE' WHERE id = {doc[0]}")

        print("Finished processing document")
        print(f"Sleeping..\n")
        time.sleep(POLLING_FREQ)
