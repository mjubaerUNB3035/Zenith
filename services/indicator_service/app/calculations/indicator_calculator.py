import pandas as pd


class IndicatorCalculator:

    # SMA - Simple Moving Average
    # Formula: SMA = (P1 + P2 + ... + Pn) / n
    def calculate_sma(
        self,
        data: list[dict],
        period: int = 20,
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        if period <= 0:
            raise ValueError("Period must be greater than zero.")

        if "close" not in dataframe.columns:
            raise ValueError("Market data must contain a close column.")

        dataframe["sma"] = (
            dataframe["close"]
            .rolling(window=period)
            .mean()
        )

        return dataframe.to_dict(
            orient="records"
        )


    # EMA - Exponential Moving Average
    # Formula: EMA = (Price × K) + (Previous EMA × (1 - K)), K = 2 / (n + 1)
    def calculate_ema(
        self,
        data: list[dict],
        period: int = 20,
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        if period <= 0:
            raise ValueError("Period must be greater than zero.")

        if "close" not in dataframe.columns:
            raise ValueError("Market data must contain a close column.")

        dataframe["ema"] = (
            dataframe["close"]
            .ewm(
                span=period,
                adjust=False,
            )
            .mean()
        )

        return dataframe.to_dict(
            orient="records"
        )


    # RSI - Relative Strength Index
    # Formula: RSI = 100 - (100 / (1 + RS)), RS = Average Gain / Average Loss
    def calculate_rsi(
        self,
        data: list[dict],
        period: int = 14,
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        if period <= 0:
            raise ValueError("Period must be greater than zero.")

        if "close" not in dataframe.columns:
            raise ValueError("Market data must contain a close column.")

        change = dataframe["close"].diff()

        gain = change.clip(lower=0)
        loss = -change.clip(upper=0)

        average_gain = gain.rolling(
            window=period
        ).mean()

        average_loss = loss.rolling(
            window=period
        ).mean()

        relative_strength = (
            average_gain / average_loss
        )

        dataframe["rsi"] = (
            100
            - (
                100
                / (
                    1
                    + relative_strength
                )
            )
        )

        return dataframe.to_dict(
            orient="records"
        )


    # VWAP - Volume Weighted Average Price
    # Formula: VWAP = Σ(Typical Price × Volume) / ΣVolume
    def calculate_vwap(
        self,
        data: list[dict],
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        required_columns = [
            "high",
            "low",
            "close",
            "volume",
        ]

        for column in required_columns:
            if column not in dataframe.columns:
                raise ValueError(
                    f"Market data must contain a {column} column."
                )

        typical_price = (
            dataframe["high"]
            + dataframe["low"]
            + dataframe["close"]
        ) / 3

        price_volume = (
            typical_price
            * dataframe["volume"]
        )

        cumulative_price_volume = (
            price_volume.cumsum()
        )

        cumulative_volume = (
            dataframe["volume"].cumsum()
        )

        dataframe["vwap"] = (
            cumulative_price_volume
            / cumulative_volume
        )

        return dataframe.to_dict(
            orient="records"
        )


    # Momentum
    # Formula: Momentum = Current Close - Close n periods ago
    def calculate_momentum(
        self,
        data: list[dict],
        period: int = 10,
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        if period <= 0:
            raise ValueError("Period must be greater than zero.")

        if "close" not in dataframe.columns:
            raise ValueError("Market data must contain a close column.")

        dataframe["momentum_indicator"] = (
            dataframe["close"]
            - dataframe["close"].shift(period)
        )

        return dataframe.to_dict(
            orient="records"
        )


    # Volatility
    # Formula: Volatility = Standard Deviation of Periodic Returns
    def calculate_volatility(
        self,
        data: list[dict],
        period: int = 20,
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        if period <= 0:
            raise ValueError("Period must be greater than zero.")

        if "close" not in dataframe.columns:
            raise ValueError("Market data must contain a close column.")

        returns = dataframe["close"].pct_change()

        dataframe["volatility_indicator"] = (
            returns
            .rolling(window=period)
            .std()
        )

        return dataframe.to_dict(
            orient="records"
        )


    # Relative Volume
    # Formula: Relative Volume = Current Volume / Average Volume
    def calculate_relative_volume(
        self,
        data: list[dict],
        period: int = 20,
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        if period <= 0:
            raise ValueError("Period must be greater than zero.")

        if "volume" not in dataframe.columns:
            raise ValueError("Market data must contain a volume column.")

        average_volume = (
            dataframe["volume"]
            .rolling(window=period)
            .mean()
        )

        dataframe["relative_volume_indicator"] = (
            dataframe["volume"]
            / average_volume
        )

        return dataframe.to_dict(
            orient="records"
        )


    # Buying Pressure
    # Formula: Buying Pressure = (Close - Low) / (High - Low)
    def calculate_buying_pressure(
        self,
        data: list[dict],
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        required_columns = [
            "high",
            "low",
            "close",
        ]

        for column in required_columns:
            if column not in dataframe.columns:
                raise ValueError(
                    f"Market data must contain a {column} column."
                )

        price_range = (
            dataframe["high"]
            - dataframe["low"]
        )

        dataframe["buying_pressure_indicator"] = (
            (dataframe["close"] - dataframe["low"])
            / price_range
        )

        return dataframe.to_dict(
            orient="records"
        )


    # Selling Pressure
    # Formula: Selling Pressure = (High - Close) / (High - Low)
    def calculate_selling_pressure(
        self,
        data: list[dict],
    ) -> list[dict]:

        dataframe = pd.DataFrame(data)

        if dataframe.empty:
            return []

        required_columns = [
            "high",
            "low",
            "close",
        ]

        for column in required_columns:
            if column not in dataframe.columns:
                raise ValueError(
                    f"Market data must contain a {column} column."
                )

        price_range = (
            dataframe["high"]
            - dataframe["low"]
        )

        dataframe["selling_pressure_indicator"] = (
            (dataframe["high"] - dataframe["close"])
            / price_range
        )

        return dataframe.to_dict(
            orient="records"
        )