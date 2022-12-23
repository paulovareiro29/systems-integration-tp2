from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import json


class API:

    def __init__(self, host, content_type="application/json"):
        self._host = host
        self._headers = {"Content-Type": content_type}

    def get(self, endpoint):
        try:
            request = Request(f"{self._host}{endpoint}", headers=self._headers)

            response = urlopen(request)
            body = response.read()

            return {
                "code": response.getcode(),
                "data": json.loads(body)
            }

        except HTTPError as e:
            return {"code": e.getcode(), "message": e.reason()}
        except URLError as e:
            return {"code": 400, "message": e.reason()}
        except:
            return {"code": 500}
