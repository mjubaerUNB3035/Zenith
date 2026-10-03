import pandas as pd


class MarketDataNormalizer:

    def normalize_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        # Standardize column names.
        data = data.copy()

        data.columns = [
            column.strip().lower()
            for column in data.columns
        ]

        return data

    def normalize_datetime(self, data: pd.DataFrame) -> pd.DataFrame:
        # Convert datetime values to pandas datetime.
        data = data.copy()

        if "datetime" in data.columns:
            data["datetime"] = pd.to_datetime(
                data["datetime"],
                errors="coerce",
            )

        return data

    def normalize_numeric(self, data: pd.DataFrame) -> pd.DataFrame:
        # Convert market values to numeric types.
        data = data.copy()

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "price_change",
            "price_change_percent",
            "trading_range",
            "average_volume",
            "average_price",
            "relative_volume",
            "buying_pressure",
            "selling_pressure",
            "momentum",
            "volatility",
        ]

        for column in numeric_columns:
            if column in data.columns:
                data[column] = pd.to_numeric(
                    data[column],
                    errors="coerce",
                )

        return data

    def normalize_invalid_values(self, data: pd.DataFrame) -> pd.DataFrame:
        # Replace infinite values with missing values.
        data = data.copy()

        data = data.replace(
            [float("inf"), float("-inf")],
            pd.NA,
        )

        return data

    def normalize_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        # Convert pandas missing values to Python None.
        data = data.copy()

        data = data.astype(object).where(
            pd.notna(data),
            None,
        )

        return data

    def remove_incomplete_market_data(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        # Remove market-data records missing required OHLC values.
        data = data.copy()

        required_columns = [
            "open",
            "high",
            "low",
            "close",
        ]

        available_columns = [
            column
            for column in required_columns
            if column in data.columns
        ]

        if available_columns:
            data = data.dropna(
                subset=available_columns
            )

        return data

    def normalize_order(self, data: pd.DataFrame) -> pd.DataFrame:
        # Sort data by symbol and datetime.
        data = data.copy()

        sort_columns = []

        if "symbol" in data.columns:
            sort_columns.append("symbol")

        if "datetime" in data.columns:
            sort_columns.append("datetime")

        if sort_columns:
            data = data.sort_values(sort_columns)

        return data.reset_index(drop=True)

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        # Run all normalization steps.
        data = self.normalize_columns(data)
        data = self.normalize_datetime(data)
        data = self.normalize_numeric(data)
        data = self.normalize_invalid_values(data)
        data = self.remove_incomplete_market_data(data)
        data = self.normalize_missing_values(data)
        data = self.normalize_order(data)

        return data