from services.screening_service.app.api.schemas.screening_schema import (
    ScreeningConfig,
    BasicScreeningConfig,
    TrendScreeningConfig,
)


def test_screening_config_defaults():
    config = ScreeningConfig()

    assert config.required_candles == 200
    assert config.basic is None
    assert config.trend is None


def test_screening_config_custom_candles():
    config = ScreeningConfig(
        required_candles=126,
    )

    assert config.required_candles == 126


def test_screening_config_with_rules():
    config = ScreeningConfig(
        required_candles=200,
        basic=BasicScreeningConfig(
            min_price=50,
            min_volume=1000000,
            min_relative_volume=1.5,
        ),
        trend=TrendScreeningConfig(
            price_above_sma=True,
            price_above_ema=True,
            positive_momentum=True,
        ),
    )

    assert config.basic.min_price == 50
    assert config.basic.min_volume == 1000000
    assert config.basic.min_relative_volume == 1.5

    assert config.trend.price_above_sma is True
    assert config.trend.price_above_ema is True
    assert config.trend.positive_momentum is True