from flask import Flask, send_file, send_from_directory, render_template
from pathlib import Path

from .api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
app.config["FRONTEND"] = Path("./frontend/")
app.config["DATABASE"] = Path("./data/stockdata.db")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
