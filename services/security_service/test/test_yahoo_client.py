from unittest.mock import patch

from shared.providers.yahoo.client import YahooClient


def test_yahoo_client_get_security_info():
    # Tests that YahooClient converts Yahoo company information
    # into the structure expected by Security Service.
    client = YahooClient()

    mock_info = {
        "longName": "Apple Inc.",
        "shortName": "Apple",
        "exchange": "NMS",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "United States",
    }

    with patch("shared.providers.yahoo.client.yf.Ticker") as mock_ticker:
        mock_ticker.return_value.info = mock_info

        result = client.get_security_info("aapl")

    mock_ticker.assert_called_once_with("AAPL")

    assert result == {
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "exchange": "NMS",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "United States",
        "active": True,
    }


def test_yahoo_client_rejects_empty_security_symbol():
    # Tests that an empty symbol is rejected before contacting Yahoo.
    client = YahooClient()

    try:
        client.get_security_info("")

        assert False

    except ValueError as exc:
        assert str(exc) == "A symbol is required."