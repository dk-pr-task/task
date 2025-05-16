""" tests/test_symbol_search.py
    
    Tests for the AlphaVantageClient symbol search endpoint.

    TODO(bugID): Refactor for using API mocking tool.

"""

from unittest.mock import patch, Mock
import pytest
import requests

from client.alpha_vantage_client import AlphaVantageClient


class TestSymbolSearchEndpoint:
    """Test class for the AlphaVantageClient symbol search endpoint."""

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_success_multiple_matches(self, mock_get, client):
        """Test successful symbol search returning multiple matches."""
        mock_response = Mock()
        keywords = "Tesla"
        expected_api_response_data = {
            "bestMatches": [
                {
                    "1. symbol": "TSLA",
                    "2. name": "Tesla Inc",
                    "3. type": "Equity",
                    "4. region": "United States",
                    "5. marketOpen": "09:30",
                    "6. marketClose": "16:00",
                    "7. timezone": "UTC-04",
                    "8. currency": "USD",
                    "9. matchScore": "1.0000",
                },
                {
                    "1. symbol": "TSCO.LON",
                    "2. name": "Tesco PLC",
                    "3. type": "Equity",
                    "4. region": "United Kingdom",
                    "5. marketOpen": "08:00",
                    "6. marketClose": "16:30",
                    "7. timezone": "Europe/London",
                    "8. currency": "GBX",
                    "9. matchScore": "0.5714",
                },
            ]
        }
        mock_response.json.return_value = expected_api_response_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = client.get_symbol_search_response(keywords)

        mock_get.assert_called_once_with(
            AlphaVantageClient.BASE_URL,
            params={
                "function": "SYMBOL_SEARCH",
                "keywords": keywords,
                "apikey": client.api_key,
            },
        )
        assert result == expected_api_response_data["bestMatches"]
        assert len(result) == 2
        assert result[0]["1. symbol"] == "TSLA"
        assert result[1]["2. name"] == "Tesco PLC"

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_success_single_match(self, mock_get, client):
        """Test successful symbol search returning a single match."""
        mock_response = Mock()
        keywords = "SingleMatchStocksymbol"
        expected_api_response_data = {
            "bestMatches": [
                {
                    "1. symbol": "SMTK",
                    "2. name": "Single Match Stock Corp",
                    "3. type": "Equity",
                    "4. region": "United States",
                    "5. marketOpen": "09:30",
                    "6. marketClose": "16:00",
                    "7. timezone": "UTC-04",
                    "8. currency": "USD",
                    "9. matchScore": "0.9500",
                }
            ]
        }
        mock_response.json.return_value = expected_api_response_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = client.get_symbol_search_response(keywords)

        mock_get.assert_called_once_with(
            AlphaVantageClient.BASE_URL,
            params={
                "function": "SYMBOL_SEARCH",
                "keywords": keywords,
                "apikey": client.api_key,
            },
        )
        assert result == expected_api_response_data["bestMatches"]
        assert len(result) == 1
        assert result[0]["1. symbol"] == "SMTK"

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_no_matches(self, mock_get, client):
        """Test symbol search successfully returning no matches."""
        mock_response = Mock()
        keywords = "XYZNONEXISTENTCOMPANY"
        # The API returns an empty list for "bestMatches" in this case.
        expected_api_response_data = {"bestMatches": []}
        mock_response.json.return_value = expected_api_response_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = client.get_symbol_search_response(keywords)

        mock_get.assert_called_once_with(
            AlphaVantageClient.BASE_URL,
            params={
                "function": "SYMBOL_SEARCH",
                "keywords": keywords,
                "apikey": client.api_key,
            },
        )
        assert result == []

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_api_error_message(self, mock_get, client):
        """Test handling of an API error message (e.g., invalid API key).

        This relies on the _make_request helper's error handling.
        """
        mock_response = Mock()
        error_data = {
            "Error Message":
            "The demo API key is invalid. Please claim your free API key."
        }
        mock_response.json.return_value = error_data
        mock_response.status_code = 200  # API errors can still return 200 OK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(
            ValueError,
            match="Alpha Vantage API Error: The demo API key is invalid."
        ):
            client.get_symbol_search_response("AnyKeyword")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_information_message_as_error(self,
                                                            mock_get, client):
        """Test handling of an "Information" message that indicates a problem.

        E.g., rate limit. This relies on the _make_request helper's error
        handling for "Information" when it's the primary content.
        """
        mock_response = Mock()
        # Example: A rate limit message might appear under "Information"
        info_data = {
            "Information": (
                "Thank you for using Alpha Vantage! Our standard API call"
                " frequency is 5 calls per minute and 500 calls per day."
            )
        }
        mock_response.json.return_value = info_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # The _make_request logic might treat a solo "Information" key as an
        # issue. Depending on the exact logic in _make_request, this might
        # need adjustment. For now, assuming it raises ValueError for a lone
        # "Information" message.
        with pytest.raises(
            ValueError,
            match="Alpha Vantage API Info: Thank you for using Alpha Vantage!"
        ):
            client.get_symbol_search_response("AnyKeyword")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_network_error(self, mock_get, client):
        """Test handling of network errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Failed to establish a new connection"
        )

        with pytest.raises(
            requests.exceptions.ConnectionError,
            match="Failed to establish a new connection",
        ):
            client.get_symbol_search_response("AnyKeyword")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_malformed_json_response(self, mock_get, client):
        """Test handling of a response that is not valid JSON."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        # Simulate requests.json() raising JSONDecodeError
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "Expecting value", "doc", 0
        )
        mock_get.return_value = mock_response

        with pytest.raises(
            ValueError,
            match="Failed to decode JSON response from Alpha Vantage API."
        ):
            client.get_symbol_search_response("AnyKeyword")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_unexpected_success_structure(self,
                                                            mock_get, client):
        """Test handling of a 200 OK response with missing 'bestMatches' key."""
        mock_response = Mock()
        # API returns 200 OK, but the expected 'bestMatches' key is missing.
        unexpected_data = {"someOtherKey": "someValue"}
        mock_response.json.return_value = unexpected_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(
            ValueError, match="Unexpected response structure for SYMBOL_SEARCH."
        ):
            client.get_symbol_search_response("AnyKeyword")

    @patch('client.alpha_vantage_client.requests.get')
    def test_get_symbol_search_empty_keywords(self, mock_get, client):
        """Test behavior when empty keywords are provided."""
        mock_response = Mock()
        keywords = ""  # Empty keywords
        # The API returns an empty list for "bestMatches" in this case.
        expected_api_response_data = {"bestMatches": []}
        mock_response.json.return_value = expected_api_response_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        result = client.get_symbol_search_response(keywords)

        mock_get.assert_called_once_with(
            AlphaVantageClient.BASE_URL,
            params={
                "function": "SYMBOL_SEARCH",
                "keywords": keywords,
                "apikey": client.api_key,
            },
        )
        assert result == []
