from pydantic import BaseModel


class IndicatorValues(BaseModel):
    sma_20: float | None = None
    ema_20: float | None = None
    rsi_14: float | None = None
    vwap: float | None = None
    momentum_10: float | None = None
    volatility_20: float | None = None
    relative_volume_20: float | None = None
    buying_pressure: float | None = None
    selling_pressure: float | None = None


class IndicatorResponse(BaseModel):
    symbol: str
    candles_used: int
    indicators: IndicatorValues