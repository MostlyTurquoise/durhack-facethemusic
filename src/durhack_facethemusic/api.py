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
        "data": [],
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
        return "Invalid date string", 404

    raise NotImplementedError()

    # get records in date range
    # turn into just column values as list
    # pass to encoder function
    # get resulting mp3 and return it
