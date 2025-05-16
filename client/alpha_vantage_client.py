""" client/alpha_vantage_client.py

    Module for the API client implementation.

"""
import requests


class AlphaVantageClient:
    """ Wraps API interaction logic.  For each endpoint, API function, it is 
    required to add a method. It encapsulats specific parameter request.

    Function names are defined as constants.
    """

    # Constants
    BASE_URL = "https://www.alphavantage.co/query"

    ERROR_MESSAGE = "Error Message"
    INFORMATION_MESSAGE = "Information"

    SHORT_TIMEOUT = 1  # Timeout to be used in request call.

    # Function names

    # Forex
    CURRENCY_EXCHANGE_RATE = "CURRENCY_EXCHANGE_RATE"
    CURRENCY_EXCHANGE_RATE_RESPONSE_KEY = "Realtime Currency Exchange Rate"

    # Core Stock APIs
    SYMBOL_SEARCH = "SYMBOL_SEARCH"
    SYMBOL_SEARCH_RESPONSE_KEY = "bestMatches"

    # Add supported function names with contants below

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key is required.")
        self.api_key = api_key

    def _make_request(self, params):
        """ Helper to make a request and return data.

        Args: Parameter list

        Returns: 
            dict: The API response data as a dictionary if successful.

        Raises:
            requests.exceptions.RequestException: For network or HTTP errors.
            ValueError: For API errors or unexpected response structure.
        """
        try:
            response = requests.get(
                self.BASE_URL, params=params, timeout=self.SHORT_TIMEOUT)
            # Raises HTTPError for bad responses (4XX or 5XX)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                raise ValueError(
                    f"Alpha Vantage API Error: {data[self.ERROR_MESSAGE]}")
            elif "Information" in data:
                if len(data.keys()) == 1:
                    raise ValueError(
                        f"Alpha Vantage API Info: {
                            data[self.INFORMATION_MESSAGE]}")
            return data

        except requests.exceptions.JSONDecodeError as err:
            raise ValueError(
                "Failed to decode JSON response from Alpha Vantage API.") from err

    def get_currency_exchange_rate_response(self, from_currency, to_currency):
        """
        Fetches the currency exchange rate between two currencies. 

        Args:
            from_currency (str): The source currency code (e.g., "USD").
            to_currency (str): The target currency code (e.g., "EUR").

        Returns:
            dict: The API response data as a dictionary if successful.

        Raises:
            requests.exceptions.RequestException: For network or HTTP errors.
            ValueError: For API errors or unexpected response structure.
        """
        params = {
            "function": self.CURRENCY_EXCHANGE_RATE,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "apikey": self.api_key,
        }

        data = self._make_request(params)
        if self.CURRENCY_EXCHANGE_RATE_RESPONSE_KEY in data:
            return data[self.CURRENCY_EXCHANGE_RATE_RESPONSE_KEY]
        else:
            raise ValueError(
                "Unexpected response structure for CURRENCY_EXCHANGE_RATE.")

    def get_symbol_search_response(self, keywords):
        """
        Searches for stock symbols matching the given keywords.

        Args:
            keywords (str): The keywords to search for (e.g., "Tesla").

        Returns:
            list: A list of matching symbols.

        Raises:
            requests.exceptions.RequestException:
                For network or HTTP errors.
            ValueError: For API errors or unexpected response structure.
        """
        params = {
            "function": self.SYMBOL_SEARCH,
            "keywords": keywords,
            "apikey": self.api_key,
        }
        data = self._make_request(params)

        if self.SYMBOL_SEARCH_RESPONSE_KEY in data:
            return data[self.SYMBOL_SEARCH_RESPONSE_KEY]
        else:
            raise ValueError(
                "Unexpected response structure for SYMBOL_SEARCH.")
