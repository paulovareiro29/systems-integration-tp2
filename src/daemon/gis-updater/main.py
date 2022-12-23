import sys
import time

from utils.api import API
import json

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

if __name__ == "__main__":

    while True:
        print(
            f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")

        # Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        api_gis = API("http://api-gis:8080")

        entities = api_gis.get(f"/api/airbnb?limit={ENTITIES_PER_ITERATION}")

        if entities["code"] != 200:
            print(entities["message"])
            time.sleep(POLLING_FREQ)
            continue

        # Use the entity information to retrieve coordinates from an external API
        api_nominatim = API("https://nominatim.openstreetmap.org")

        for airbnb in entities["data"]:
            res = api_nominatim.get(
                f"/reverse?format=json&lat={airbnb['latitude']}&lon={airbnb['longitude']}")

            if res["code"] != 200:
                continue

            data = res["data"]

            house_number = data["address"].get("house_number") or ""
            road = data["address"].get("road") or ""

            street = f"{house_number}, {road}"
            if street.startswith(","):
                street = street.replace(",", "").strip()

            print(street)

            # Submit the changes
            updated = api_gis.put(
                f"/api/airbnb/{airbnb['id']}", {"street": street})

            if updated["code"] == 200:
                print("Updated Successfuly!")

        time.sleep(POLLING_FREQ)
