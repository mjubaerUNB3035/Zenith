import pandas as pd

from services.market_data_service.app.normalization.market_data_normalizer import (
    MarketDataNormalizer,
)


def test_normalize_columns():
    data = pd.DataFrame(
        {
            " Symbol ": ["AAPL"],
            " Close ": [100.0],
        }
    )

    normalizer = MarketDataNormalizer()

    result = normalizer.normalize_columns(data)

    assert list(result.columns) == ["symbol", "close"]


def test_normalize_datetime():
    data = pd.DataFrame(
        {
            "datetime": ["2026-09-10 10:00:00"],
        }
    )

    normalizer = MarketDataNormalizer()

    result = normalizer.normalize_datetime(data)

    assert pd.api.types.is_datetime64_any_dtype(
        result["datetime"]
    )


def test_normalize_numeric():
    data = pd.DataFrame(
        {
            "close": ["100.50"],
            "volume": ["500000"],
        }
    )

    normalizer = MarketDataNormalizer()

    result = normalizer.normalize_numeric(data)

    assert result["close"].iloc[0] == 100.50
    assert result["volume"].iloc[0] == 500000


def test_normalize_invalid_values():
    data = pd.DataFrame(
        {
            "close": [100.0, float("inf"), float("-inf")],
        }
    )

    normalizer = MarketDataNormalizer()

    result = normalizer.normalize_invalid_values(data)

    assert pd.isna(result["close"].iloc[1])
    assert pd.isna(result["close"].iloc[2])


def test_normalize_missing_values():
    data = pd.DataFrame(
        {
            "price_change": [1.5, float("nan")],
        }
    )

    normalizer = MarketDataNormalizer()

    result = normalizer.normalize_missing_values(data)

    assert result["price_change"].iloc[0] == 1.5
    assert result["price_change"].iloc[1] is None


def test_normalize_order():
    data = pd.DataFrame(
        {
            "symbol": ["MSFT", "AAPL", "AAPL"],
            "datetime": [
                "2026-09-10 11:00:00",
                "2026-09-10 11:00:00",
                "2026-09-10 10:00:00",
            ],
        }
    )

    normalizer = MarketDataNormalizer()

    result = normalizer.normalize_datetime(data)
    result = normalizer.normalize_order(result)

    assert result.iloc[0]["symbol"] == "AAPL"
    assert result.iloc[0]["datetime"].hour == 10


def test_normalize():
    data = pd.DataFrame(
        {
            " Symbol ": ["MSFT", "AAPL"],
            " Close ": ["200.0", "100.0"],
            " Volume ": ["500000", "1000000"],
            "datetime": [
                "2026-09-10 11:00:00",
                "2026-09-10 10:00:00",
            ],
            "price_change": [1.0, float("nan")],
        }
    )

    normalizer = MarketDataNormalizer()

    result = normalizer.normalize(data)

    assert list(result.columns) == [
        "symbol",
        "close",
        "volume",
        "datetime",
        "price_change",
    ]

    assert result.iloc[0]["symbol"] == "AAPL"
    assert result.iloc[0]["close"] == 100.0
    assert result.iloc[0]["price_change"] is None