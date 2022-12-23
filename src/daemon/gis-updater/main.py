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

        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        api_gis = API("http://api-gis:8080")

        entities = api_gis.get(f"/api/airbnbs?limit={ENTITIES_PER_ITERATION}")

        if entities["code"] != 200:
            time.sleep(POLLING_FREQ)
            continue

        for airbnb in entities["data"]:
            print(airbnb["latitude"], airbnb["longitude"])
        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        # !TODO: 3- Submit the changes
        time.sleep(POLLING_FREQ)
