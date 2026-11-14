from flask import Flask, send_file, send_from_directory
from pathlib import Path

from .api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
app.config["FRONTEND"] = Path("./frontend/")
app.config["DATABASE"] = Path("./data/stockdata.db")


@app.route("/")
def index():
    return send_file("./frontend/index.html")


@app.route("/<path:name>")
def static_files(name):
    return send_from_directory(app.config["FRONTEND"], name)
