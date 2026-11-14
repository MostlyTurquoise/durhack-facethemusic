from flask import Blueprint, request
import datetime as dt

api = Blueprint("api", __name__)


@api.route("/get_data")
def show():
    try:
        start_timestamp = dt.datetime.fromisoformat(
            request.args.get("from", default="")
        )
        end_timestamp = dt.datetime.fromisoformat(request.args.get("to", default=""))
    except ValueError:
        return {"error": "Invalid date string(s)"}, 404

    return {
        "from": start_timestamp.isoformat(),
        "to": end_timestamp.isoformat(),
        "data": {},
    }
