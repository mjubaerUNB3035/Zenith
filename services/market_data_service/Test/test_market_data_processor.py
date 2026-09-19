import pandas as pd

from services.market_data_service.app.processing.market_data_processor import (
    MarketDataProcessor,
)


def test_market_data_processor():
    data = pd.DataFrame({
        "Open": [100, 102, 104, 103, 105],
        "High": [103, 105, 107, 106, 108],
        "Low": [99, 101, 102, 101, 103],
        "Close": [102, 104, 106, 105, 107],
        "Volume": [1000, 1200, 1500, 1300, 1600],
    })

    processor = MarketDataProcessor()

    result = processor.process(data)

    assert "PriceChange" in result.columns
    assert "PriceChangePercent" in result.columns
    assert "TradingRange" in result.columns
    assert "AverageVolume" in result.columns
    assert "AveragePrice" in result.columns
    assert "RelativeVolume" in result.columns
    assert "BuyingPressure" in result.columns
    assert "SellingPressure" in result.columns
    assert "Momentum" in result.columns
    assert "Volatility" in result.columns