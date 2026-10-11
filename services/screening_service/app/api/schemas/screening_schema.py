from pydantic import BaseModel


class BasicScreeningConfig(BaseModel):
    min_price: float | None = None
    max_price: float | None = None
    min_volume: int | None = None
    min_relative_volume: float | None = None
    min_momentum: float | None = None
    min_volatility: float | None = None


class TrendScreeningConfig(BaseModel):
    price_above_sma: bool = False
    price_above_ema: bool = False
    positive_momentum: bool = False


class MomentumScreeningConfig(BaseModel):
    min_rsi: float | None = None
    max_rsi: float | None = None
    positive_momentum: bool = False
    min_relative_volume: float | None = None


class VolumeScreeningConfig(BaseModel):
    min_relative_volume: float | None = None
    volume_above_average: bool = False


class PressureScreeningConfig(BaseModel):
    min_buying_pressure: float | None = None
    max_selling_pressure: float | None = None
    buying_pressure_dominant: bool = False


class VolatilityScreeningConfig(BaseModel):
    min_volatility: float | None = None
    max_volatility: float | None = None


class ScreeningConfig(BaseModel):
    required_candles: int = 200

    basic: BasicScreeningConfig | None = None
    trend: TrendScreeningConfig | None = None
    momentum: MomentumScreeningConfig | None = None
    volume: VolumeScreeningConfig | None = None
    pressure: PressureScreeningConfig | None = None
    volatility: VolatilityScreeningConfig | None = None