import pandas as pd

from services.market_data_service.app.processing.market_data_processor import (
    MarketDataProcessor,
)


def test_market_data_processor():
    data = pd.DataFrame({
        "symbol": ["AAPL", "AAPL", "AAPL", "AAPL", "AAPL"],
        "open": [100, 102, 104, 103, 105],
        "high": [103, 105, 107, 106, 108],
        "low": [99, 101, 102, 101, 103],
        "close": [102, 104, 106, 105, 107],
        "volume": [1000, 1200, 1500, 1300, 1600],
        "datetime": pd.date_range(
            "2026-01-01",
            periods=5,
            freq="h",
        ),
    })

    processor = MarketDataProcessor()

    result = processor.process(data)

    assert "price_change" in result.columns
    assert "price_change_percent" in result.columns
    assert "trading_range" in result.columns
    assert "average_volume" in result.columns
    assert "average_price" in result.columns
    assert "relative_volume" in result.columns
    assert "buying_pressure" in result.columns
    assert "selling_pressure" in result.columns
    assert "momentum" in result.columns
    assert "volatility" in result.columns