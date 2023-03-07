from flask import Flask, jsonify
from time import sleep
import json

app = Flask(__name__)


@app.route("/search", methods=["POST"])
def page_search():
    # Simulate delay of 60 seconds
    sleep(60)

    # Load data from JSON file
    with open("response_b.json") as f:
        response_data = json.load(f)

    # Return response as JSON
    return jsonify(response_data)
