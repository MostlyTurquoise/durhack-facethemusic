from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Face the Music!</h1> <p>Hello, Test!</p>"
