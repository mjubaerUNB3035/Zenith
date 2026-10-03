from services.indicator_service.app.clients.market_data_client import (
    MarketDataClient,
)


def test_get_market_data_for_indicator():
    client = MarketDataClient()

    data = client.get_market_data_for_indicator(
        symbol="AAPL",
        required_candles=5,
    )

    assert len(data) == 5
    assert all(record["symbol"] == "AAPL" for record in data)
    assert all(record["interval"] == "1d" for record in data)