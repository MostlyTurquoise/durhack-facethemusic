from flask import Blueprint, request, current_app
import datetime as dt
import sqlite3

api = Blueprint("api", __name__)


@api.route("/get_data")
def get_data():
    try:
        start_timestamp = dt.datetime.fromisoformat(
            request.args.get("from", default="")
        )
        end_timestamp = dt.datetime.fromisoformat(request.args.get("to", default=""))
    except ValueError:
        return {"error": "Invalid date string(s)"}, 400

    try:
        with sqlite3.connect(current_app.config["DATABASE"]) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT timestamp, open 
                FROM eurusd 
                WHERE unixepoch(timestamp) >= unixepoch(?) 
                AND unixepoch(timestamp) < unixepoch(?)
                ORDER BY unixepoch(timestamp) ASC
                """,
                (start_timestamp, end_timestamp),
            )
            rows = cursor.fetchall()
            first_val_timestamp = rows[0][0]
            last_val_timestamp = rows[-1][0]
            result = [v for (t, v) in rows]
    except sqlite3.OperationalError as e:
        print("Error occured:", e)
        return {"error": str(e)}, 400

    return {
        "from": first_val_timestamp,
        "to": last_val_timestamp,
        "data": result,
    }


@api.route("/transform")
def transform():
    """
    `/transform` endpoint handler. Takes two url-encoded parameters `from` and `to`,
    extracts the data from the database, passes it to the encoder, and then returns
    the resulting mp3 as the response to the request.
    """

    try:
        start_timestamp = dt.datetime.fromisoformat(
            request.args.get("from", default="")
        )
        end_timestamp = dt.datetime.fromisoformat(request.args.get("to", default=""))
    except ValueError:
        return "Invalid date string", 400

    try:
        with sqlite3.connect(current_app.config["DATABASE"]) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT timestamp, open 
                FROM eurusd 
                WHERE unixepoch(timestamp) >= unixepoch(?) 
                AND unixepoch(timestamp) < unixepoch(?)
                ORDER BY unixepoch(timestamp) ASC
                """,
                (start_timestamp, end_timestamp),
            )
            rows = cursor.fetchall()
            result = [v for (t, v) in rows]
    except sqlite3.OperationalError as e:
        print("Error occured:", e)
        return "Error: " + str(e), 400

    raise NotImplementedError()

    # pass to encoder function
    # get resulting mp3 and return it
