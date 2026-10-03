import math

from fastapi import APIRouter

from services.indicator_service.app.clients.market_data_client import (
    MarketDataClient,
)
from services.indicator_service.app.calculations.indicator_calculator import (
    IndicatorCalculator,
)
from services.indicator_service.app.api.schemas.indicator_schema import (
    IndicatorResponse,
)


router = APIRouter(
    prefix="/indicators",
    tags=["Indicators"],
)


def get_latest_value(
    data: list[dict],
    field: str,
):
    if not data:
        return None

    value = data[-1].get(field)

    if value is None:
        return None

    if isinstance(value, float) and (
        math.isnan(value) or math.isinf(value)
    ):
        return None

    return value


@router.get(
    "/{symbol}",
    response_model=IndicatorResponse,
)
def get_indicators(
    symbol: str,
    candles: int = 200,
):
    # Get market data from the Market Data Service.

    market_data_client = MarketDataClient()

    market_data = market_data_client.get_market_data_for_indicator(
        symbol=symbol,
        required_candles=candles,
    )

    # Create the indicator calculator.

    calculator = IndicatorCalculator()

    # Calculate all indicators.

    sma = calculator.calculate_sma(
        data=market_data,
        period=20,
    )

    ema = calculator.calculate_ema(
        data=market_data,
        period=20,
    )

    rsi = calculator.calculate_rsi(
        data=market_data,
        period=14,
    )

    vwap = calculator.calculate_vwap(
        data=market_data,
    )

    momentum = calculator.calculate_momentum(
        data=market_data,
        period=10,
    )

    volatility = calculator.calculate_volatility(
        data=market_data,
        period=20,
    )

    relative_volume = calculator.calculate_relative_volume(
        data=market_data,
        period=20,
    )

    buying_pressure = calculator.calculate_buying_pressure(
        data=market_data,
    )

    selling_pressure = calculator.calculate_selling_pressure(
        data=market_data,
    )

    return {
        "symbol": symbol.strip().upper(),
        "candles_used": len(market_data),
        "indicators": {
            "sma_20": get_latest_value(
                sma,
                "sma",
            ),
            "ema_20": get_latest_value(
                ema,
                "ema",
            ),
            "rsi_14": get_latest_value(
                rsi,
                "rsi",
            ),
            "vwap": get_latest_value(
                vwap,
                "vwap",
            ),
            "momentum_10": get_latest_value(
                momentum,
                "momentum_indicator",
            ),
            "volatility_20": get_latest_value(
                volatility,
                "volatility_indicator",
            ),
            "relative_volume_20": get_latest_value(
                relative_volume,
                "relative_volume_indicator",
            ),
            "buying_pressure": get_latest_value(
                buying_pressure,
                "buying_pressure_indicator",
            ),
            "selling_pressure": get_latest_value(
                selling_pressure,
                "selling_pressure_indicator",
            ),
        },
    }