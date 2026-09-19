from unittest.mock import patch

from services.market_data_service.app.providers.yahoo.client import YahooClient


def test_yahoo_client_requests_multiple_symbols():
    # Tests that YahooClient sends multiple symbols to yfinance in one bulk request.
    # YahooClient comes from app.providers.yahoo.client.
    # yfinance is mocked so this test does not make a real external request.
    client = YahooClient()

    with patch(
        "services.market_data_service.app.providers.yahoo.client.yf.download"
    ) as mock_download:

        mock_download.return_value = {"AAPL": "data", "MSFT": "data"}

        result = client.get_market_data(
            symbols=["AAPL", "MSFT"],
            period="5d",
            interval="1h",
        )

    mock_download.assert_called_once_with(
        tickers=["AAPL", "MSFT"],
        period="5d",
        interval="1h",
        group_by="ticker",
        auto_adjust=False,
        progress=False,
    )

    assert result == {"AAPL": "data", "MSFT": "data"}


def test_yahoo_client_rejects_empty_symbols():
    # Tests that YahooClient refuses an empty symbol list before contacting Yahoo.
    # No external provider call should occur when the input is invalid.
    client = YahooClient()

    try:
        client.get_market_data([])
        assert False
    except ValueError as exc:
        assert str(exc) == "At least one symbol is required."