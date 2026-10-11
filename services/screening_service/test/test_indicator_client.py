from services.screening_service.app.clients.indicator_client import (
    IndicatorClient,
)


def test_get_indicators():
    client = IndicatorClient()

    data = client.get_indicators(
        symbol="AAPL",
        candles=5,
    )

    assert data["symbol"] == "AAPL"
    assert data["candles_used"] == 5
    assert "indicators" in data