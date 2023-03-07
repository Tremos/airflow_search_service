import uuid
from flask import Flask, jsonify, Response
from flask_crontab import Crontab
import threading
from utils import (
    write_search_id,
    write_search_data_a,
    write_search_data_b,
    load_search_status,
    load_exchange_rate,
)

app = Flask(__name__)
cron = Crontab(app)


@app.before_first_request
def startup() -> None:
    load_exchange_rate()


@app.route("/search", methods=["POST"])
def page_search() -> Response:
    """
    A POST route that generates a unique search ID and starts two threads to write search data.

    :return: JSON response with the generated search ID.
    """

    # Generate unique search ID
    search_id = str(uuid.uuid4())
    write_search_id(search_id)

    threading.Thread(target=write_search_data_a, args=(search_id,)).start()
    threading.Thread(target=write_search_data_b, args=(search_id,)).start()

    # Return search ID in JSON format
    return jsonify({"search_id": search_id})


@app.route("/request/<search_id>/<currency>/", methods=["GET"])
def page_request(search_id: str, currency: str) -> Response:
    """
    A GET route that returns the status of a search given its ID and currency.

    :param search_id: The ID of the search to retrieve the status of.
    :param currency: The currency to retrieve the status of.
    :return: The status of the search as a JSON string.
    """

    status = load_search_status(search_id, currency)

    return status
    # return jsonify(search_id)


@cron.job(minute="0", hour="12")
def scheduled_exchange_load() -> None:
    """
    A scheduled job that runs every day at 12:00 to load exchange rates.
    """
    load_exchange_rate()
