import math

from services.indicator_service.app.calculations.indicator_calculator import (
    IndicatorCalculator,
)


def create_test_data():
    return [
        {
            "symbol": "AAPL",
            "datetime": f"2026-01-{day:02d}",
            "open": 100 + day,
            "high": 105 + day,
            "low": 95 + day,
            "close": 102 + day,
            "volume": 1000000 + (day * 10000),
        }
        for day in range(1, 31)
    ]


def test_calculate_sma():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_sma(
        data=data,
        period=20,
    )

    assert len(result) == 30
    assert math.isnan(result[0]["sma"])
    assert not math.isnan(result[19]["sma"])


def test_calculate_ema():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_ema(
        data=data,
        period=20,
    )

    assert len(result) == 30
    assert not math.isnan(result[19]["ema"])


def test_calculate_rsi():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_rsi(
        data=data,
        period=14,
    )

    assert len(result) == 30
    assert not math.isnan(result[14]["rsi"])
    assert 0 <= result[14]["rsi"] <= 100


def test_calculate_vwap():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_vwap(
        data=data,
    )

    assert len(result) == 30
    assert result[0]["vwap"] > 0


def test_calculate_momentum():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_momentum(
        data=data,
        period=10,
    )

    assert len(result) == 30
    assert math.isnan(result[0]["momentum_indicator"])
    assert not math.isnan(result[10]["momentum_indicator"])


def test_calculate_volatility():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_volatility(
        data=data,
        period=20,
    )

    assert len(result) == 30
    assert not math.isnan(result[20]["volatility_indicator"])


def test_calculate_relative_volume():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_relative_volume(
        data=data,
        period=20,
    )

    assert len(result) == 30
    assert not math.isnan(
        result[19]["relative_volume_indicator"]
    )


def test_calculate_buying_pressure():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_buying_pressure(
        data=data,
    )

    assert len(result) == 30
    assert 0 <= result[0]["buying_pressure_indicator"] <= 1


def test_calculate_selling_pressure():
    calculator = IndicatorCalculator()
    data = create_test_data()

    result = calculator.calculate_selling_pressure(
        data=data,
    )

    assert len(result) == 30
    assert 0 <= result[0]["selling_pressure_indicator"] <= 1