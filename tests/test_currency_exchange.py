""" tests/test_currency_exchange.py

    Tests for the Currency Exchange Endpount.

    To add more coverage, parameterized tests can be generated to cover more
    permutations of test input parameter.

    To increase readability, mock data should be factored out into a test_data
    directory. This will improve readability further, especially when adding
    more test cases.

    TODO(bugID): Refactor for using API mocking tool.
"""

from unittest.mock import patch, Mock
import pytest
import requests
from client.alpha_vantage_client import AlphaVantageClient


class TestCurrencyExchangeRate:
    """Tests for the CURRENCY_EXCHANGE_RATE endpoint of AlphaVantageClient.

    Scenario Coverage:
        test_get_currency_exchange_rate_success:
            Happy path, successful API response.
        test_get_currency_exchange_rate_api_error:
            Handles Alpha Vantage specific error messages in the JSON response.
        test_get_currency_exchange_rate_premium_endpoint_info:
            Handles "Information" messages, typically for premium features.
        test_get_currency_exchange_rate_network_error:
            Simulates `requests` library exceptions like ConnectionError.
        test_get_currency_exchange_rate_malformed_json:
            Simulates scenarios where the API returns invalid JSON.
        test_get_currency_exchange_rate_unexpected_success_structure:
            Simulates a 200 OK response with an unexpected JSON structure.
        test_client_initialization_no_api_key:
            Ensures the client requires an API key for initialization.
    """

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_currency_exchange_rate_success(self, mock_get, client):
        """Tests successful retrieval of an exchange rate."""
        mock_response = Mock()
        expected_data = {
            "Realtime Currency Exchange Rate": {
                "1. From_Currency Code": "USD",
                "2. From_Currency Name": "United States Dollar",
                "3. To_Currency Code": "EUR",
                "4. To_Currency Name": "Euro",
                "5. Exchange Rate": "0.92500000",
                "6. Last Refreshed": "2025-05-16 08:00:00",
                "7. Time Zone": "UTC",
                "8. Bid Price": "0.92490000",
                "9. Ask Price": "0.92510000"
            }
        }
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()  # Ensure no HTTPError is raised
        mock_get.return_value = mock_response

        from_currency = "USD"
        to_currency = "EUR"
        result = client.get_currency_exchange_rate_response(
            from_currency, to_currency)

        mock_get.assert_called_once_with(
            AlphaVantageClient.BASE_URL,
            params={
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_currency,
                "to_currency": to_currency,
                "apikey": client.api_key,
            })
        assert result == expected_data["Realtime Currency Exchange Rate"]
        assert result["1. From_Currency Code"] == from_currency
        assert result["3. To_Currency Code"] == to_currency

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_currency_exchange_rate_api_error(self, mock_get, client):
        """Tests handling of an API error message from Alpha Vantage."""
        mock_response = Mock()
        error_data = {
            "Error Message": "Invalid API call. Please check your parameters."
        }
        mock_response.json.return_value = error_data
        mock_response.status_code = 200  # API errors can still return 200 OK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(
                ValueError,
                match="Alpha Vantage API Error: Invalid API call"):
            client.get_currency_exchange_rate_response("UXD", "EUR")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_currency_exchange_rate_premium_endpoint_info(
            self, mock_get, client):
        """Tests handling of 'Information' messages."""
        mock_response = Mock()
        info_data = {
            "Information":
                "Thank you for using Alpha Vantage! This is a premium endpoint."
        }
        mock_response.json.return_value = info_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(
                ValueError,
                match=(
                    "Alpha Vantage API Info: "
                    "Thank you for using Alpha Vantage! "
                    "This is a premium endpoint.")):
            client.get_currency_exchange_rate_response("USD", "EUR")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_currency_exchange_rate_network_error(self, mock_get, client):
        """Tests handling of network errors (e.g., connection timeout)."""
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Failed to connect")

        with pytest.raises(requests.exceptions.ConnectionError,
                           match="Failed to connect"):
            client.get_currency_exchange_rate_response("USD", "EUR")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_currency_exchange_rate_malformed_json(self, mock_get, client):
        """Tests handling of a response with malformed JSON."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "Error decoding JSON", "doc", 0)
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Failed to decode JSON response"):
            client.get_currency_exchange_rate_response("USD", "EUR")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_currency_exchange_rate_unexpected_success_structure(
            self, mock_get, client):
        """Tests a 200 OK response with an unexpected JSON structure."""
        mock_response = Mock()
        unexpected_data = {"UnexpectedKey": "UnexpectedValue"}
        mock_response.json.return_value = unexpected_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(
            ValueError,
            match="Unexpected response structure for CURRENCY_EXCHANGE_RATE."
        ):
            client.get_currency_exchange_rate_response("USD", "EUR")

    def test_client_initialization_no_api_key(self):
        """Tests client raises ValueError if no API key is provided."""
        with pytest.raises(ValueError, match="API key is required."):
            AlphaVantageClient(api_key=None)
        with pytest.raises(ValueError, match="API key is required."):
            AlphaVantageClient(api_key="")
