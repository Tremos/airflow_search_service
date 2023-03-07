import requests
import json
from config import BASE_DIR
from flask import jsonify, Response
import datetime
import xmltodict
from dao.currency_dao import CurrenciesDAO
from typing import Dict, Any, List


def load_data(filename: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.

    :param filename: The name of the file to load data from.
    :return A dictionary with the loaded data.
    """
    with open(f"./data/{filename}.json", "r") as f:
        data = json.load(f)
    return data


def write_data(filename: str, data: Dict[str, Any] | List[Dict[str, Any]]) -> None:
    """
    Write JSON data to a file.

    :param filename: The name of the file to write data to.
    :param data: The data to write to the file.
    """
    with open(f"./data/{filename}.json", "w") as f:
        json.dump(data, f)


def write_search_id(search_id: str) -> None:
    """
    Create a new search entry with the given search ID.

    :param search_id: The ID of the search to create.
    """
    search_data = dict(search_id=search_id, status="PENDING", items=[])
    write_data(search_id, search_data)


def write_search_data_a(search_id: str) -> None:
    """
    Fetch flight search results from provider A and write them to the search database.

    :param search_id: The ID of the search to fetch results for.
    """
    provider_a_response = requests.post("http://provider_a:9001/search").json()

    data = load_data(search_id)

    if data["items"]:
        data["status"] = "COMPLETED"
    data["items"] += provider_a_response
    # Store search request data in JSON file
    write_data(search_id, data)


def write_search_data_b(search_id: str) -> None:
    """
    Fetch flight search results from provider B and write them to the search database.

    :param search_id: The ID of the search to fetch results for.
    """

    provider_b_response = requests.post("http://provider_b:9002/search").json()

    data = load_data(search_id)

    if data["items"]:
        data["status"] = "COMPLETED"
    data["items"] += provider_b_response
    # Store search request data in JSON file
    write_data(search_id, data)


def load_search_status(search_id: str, currency_to: str) -> Response | Dict[str, str]:
    """
    Load flight search results from the search database,
    convert prices to the requested currency, and return the results.

    :param search_id: The ID of the search to load results from.
    :param currency_to: The currency to convert flight prices to.
    :return: A response object with the flight search results in the requested currency,
    or a dictionary with an error message if the currency is not supported.
    """
    currency_to = currency_to.upper()
    if currency_to != "KZT":
        return {"status": "Oops, looks like we doesn't have that currency)"}

    data = load_data(search_id)

    search_items = data.get("items")

    # Create a set of currency names from the search items
    currencies_from = {
        currency.get("pricing").get("currency") for currency in search_items
    }

    currency_rate_dict = get_currency_rate(currencies_from)

    for item in search_items:
        flight_currency_name = item.get("pricing").get("currency").upper()
        flight_total = float(item.get("pricing").get("total"))

        if flight_currency_name is None or flight_total is None:
            continue

        if flight_currency_name != currency_to:
            rate = currency_rate_dict.get(f"{flight_currency_name}")
            if rate is None:
                continue
            rate = float(rate)
        else:
            rate = 1

        amount = rate * flight_total
        item["price"] = dict(amount=f"{amount:.2f}", currency=currency_to)

    # Sorting items by "total" price
    sorted_items = sorted(
        search_items, key=lambda item: float(item.get("price").get("amount"))
    )

    data["items"] = sorted_items

    write_data(search_id, data)

    return jsonify(data)


def get_currency_rate(currencies_from: set[str]) -> Dict[str, float]:
    """
    Get the exchange rates for a set of currencies from the database.

    :param currencies_from: The set of currency names to get exchange rates for.
    :return: A dictionary mapping currency names to exchange rates.
    """
    today = datetime.date.today().strftime("%d-%m-%Y")

    currencies_dao = CurrenciesDAO(f"{BASE_DIR}/data/{today}.json")

    currency_rate_dict = {}

    for currency_from in currencies_from:
        currency_dict = currencies_dao.get_by_currency_name(currency_from)
        if currency_dict is None:
            continue
        currency_rate_dict[currency_dict.get("title")] = currency_dict.get("rate")

    return currency_rate_dict


def load_exchange_rate() -> None:
    """
    Fetch the current exchange rates from the national bank website and write them to the exchange rate database.
    """
    today = datetime.date.today().strftime("%d-%m-%Y")

    url = f"https://www.nationalbank.kz/rss/get_rates.cfm?fdate={today}"
    response = requests.get(url)

    # parse XML data into dictionary
    data_dict = xmltodict.parse(response.content)

    rates_data = []

    for item in data_dict.get("rates").get("item"):
        rates_data.append(dict(title=item.get("title"), rate=item.get("description")))

    exchange_rate_data = rates_data

    write_data(today, exchange_rate_data)
