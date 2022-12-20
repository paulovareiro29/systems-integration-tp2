import sys
from flask import Flask

from routes import bpArea, bpType, bpHost, bpAirbnb

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

app.register_blueprint(bpArea, url_prefix="/api/area")
app.register_blueprint(bpType, url_prefix="/api/type")
app.register_blueprint(bpHost, url_prefix="/api/host")
app.register_blueprint(bpAirbnb, url_prefix="/api/airbnb")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
