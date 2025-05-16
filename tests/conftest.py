# tests/conftest.py
import pytest
from client.alpha_vantage_client import AlphaVantageClient

@pytest.fixture
def api_key():
    """Provides a dummy API key for testing."""
    return "TESTAPIKEY123"

@pytest.fixture
def client(api_key):
    """Provides an instance of the AlphaVantageClient."""
    return AlphaVantageClient(api_key=api_key)