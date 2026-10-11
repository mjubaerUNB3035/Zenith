from services.screening_service.app.api.schemas.screening_schema import (
    TrendScreeningConfig,
)
from services.screening_service.app.screening.trend_screening import (
    TrendScreening,
)


def test_trend_screening_passes():
    screening = TrendScreening()

    config = TrendScreeningConfig(
        price_above_sma=True,
        price_above_ema=True,
        positive_momentum=True,
    )

    data = {
        "price": 100,
        "sma_20": 95,
        "ema_20": 97,
        "momentum": 5,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is True
    assert all(result["rules"].values())


def test_trend_screening_fails():
    screening = TrendScreening()

    config = TrendScreeningConfig(
        price_above_sma=True,
    )

    data = {
        "price": 90,
        "sma_20": 95,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is False
    assert result["rules"]["price_above_sma"] is False


def test_trend_screening_skips_unrequested_rules():
    screening = TrendScreening()

    config = TrendScreeningConfig(
        positive_momentum=True,
    )

    data = {
        "momentum": 5,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert "positive_momentum" in result["rules"]
    assert "price_above_sma" not in result["rules"]
    assert "price_above_ema" not in result["rules"]