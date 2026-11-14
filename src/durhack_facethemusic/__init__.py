from .server import app


def main() -> None:
    print("Hello from durhack-facethemusic!")
    print("Running on http://0.0.0.0:5000")
    app.run("0.0.0.0", 5000, debug=True)
