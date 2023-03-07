import json
from typing import List, Dict, Any


class CurrenciesDAO:
    """
    A class that represents a data access object for currencies.

    :param path: A string that represents the path to the JSON
                 file that contains currency data.
    """

    def __init__(self, path: str) -> None:
        self.path = path

    def load_data(self) -> List[Dict[str, Any]]:
        """
        A method that loads currency data from the JSON file
        specified in the `path` attribute.

        :return: A dictionary that represents currency data.
        """
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_all(self) -> List[Dict[str, Any]]:
        """
        A method that retrieves all currency data from the JSON file
        specified in the `path` attribute.

        :return: A dictionary that represents currency data.
        """
        currencies = self.load_data()
        return currencies

    def get_by_currency_name(self, currency_name: str) -> Dict[str, Any] | None:
        """
        A method that retrieves currency data for a specific currency from the
        JSON file specified in the `path` attribute.

        :param currency_name: A string that represents the name of the
                              currency to retrieve.
        :return: A dictionary that represents currency data, or `None` if the
                 specified currency is not found.
        """
        currencies = self.load_data()
        for currency in currencies:
            if currency.get("title") == currency_name:
                return currency
