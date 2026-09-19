import pandas as pd


class MarketDataProcessor:

    def process_price(self, data: pd.DataFrame) -> pd.DataFrame:
        # Calculate price changes and trading range.
        data = data.copy()

        data["price_change"] = (
            data.groupby("symbol")["close"]
            .diff()
        )

        data["price_change_percent"] = (
            data.groupby("symbol")["close"]
            .pct_change()
            * 100
        )

        data["trading_range"] = (
            data["high"] - data["low"]
        )

        return data

    def process_volume(self, data: pd.DataFrame) -> pd.DataFrame:
        # Calculate the 20-period average volume.
        data = data.copy()

        data["average_volume"] = (
            data.groupby("symbol")["volume"]
            .transform(
                lambda values: values.rolling(
                    window=20,
                    min_periods=1,
                ).mean()
            )
        )

        return data

    def process_average_price(self, data: pd.DataFrame) -> pd.DataFrame:
        # Calculate the average price using OHLC.
        data = data.copy()

        data["average_price"] = (
            data["open"]
            + data["high"]
            + data["low"]
            + data["close"]
        ) / 4

        return data

    def process_relative_volume(self, data: pd.DataFrame) -> pd.DataFrame:
        # Compare current volume with average volume.
        data = data.copy()

        data["relative_volume"] = (
            data["volume"] / data["average_volume"]
        )

        return data

    def process_buying_pressure(self, data: pd.DataFrame) -> pd.DataFrame:
        # Measure where the close sits within the trading range.
        data = data.copy()

        price_range = data["high"] - data["low"]

        data["buying_pressure"] = (
            (data["close"] - data["low"]) / price_range
        ).fillna(0)

        return data

    def process_selling_pressure(self, data: pd.DataFrame) -> pd.DataFrame:
        # Measure selling pressure within the trading range.
        data = data.copy()

        price_range = data["high"] - data["low"]

        data["selling_pressure"] = (
            (data["high"] - data["close"]) / price_range
        ).fillna(0)

        return data

    def process_momentum(self, data: pd.DataFrame) -> pd.DataFrame:
        # Calculate 10-period price momentum.
        data = data.copy()

        data["momentum"] = (
            data.groupby("symbol")["close"]
            .diff(10)
        )

        return data

    def process_volatility(self, data: pd.DataFrame) -> pd.DataFrame:
        # Calculate rolling volatility from price changes.
        data = data.copy()

        price_change = (
            data.groupby("symbol")["close"]
            .pct_change()
        )

        data["volatility"] = (
            price_change.groupby(data["symbol"])
            .transform(
                lambda values: values.rolling(
                    window=20,
                    min_periods=1,
                ).std()
            )
        )

        return data

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        # Run all market data processing steps.
        data = data.copy()

        data = data.sort_values(
            ["symbol", "datetime"]
        ).reset_index(drop=True)

        data = self.process_price(data)
        data = self.process_volume(data)
        data = self.process_average_price(data)
        data = self.process_relative_volume(data)
        data = self.process_buying_pressure(data)
        data = self.process_selling_pressure(data)
        data = self.process_momentum(data)
        data = self.process_volatility(data)

        return data