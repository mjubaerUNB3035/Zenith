import pandas as pd


class MarketDataNormalizer:

    def normalize_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.copy()

        data.columns = [
            column.strip().lower()
            for column in data.columns
        ]

        return data

    def normalize_datetime(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.copy()

        if "datetime" in data.columns:
            data["datetime"] = pd.to_datetime(
                data["datetime"],
                errors="coerce",
            )

        return data

    def normalize_numeric(self, data: pd.DataFrame) -> pd.DataFrame:
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
        data = data.copy()

        data = data.replace(
            [float("inf"), float("-inf")],
            pd.NA,
        )

        return data

    def normalize_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.copy()

        data = data.astype(object).where(
            pd.notna(data),
            None,
        )

        return data

    def normalize_order(self, data: pd.DataFrame) -> pd.DataFrame:
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
        data = self.normalize_columns(data)
        data = self.normalize_datetime(data)
        data = self.normalize_numeric(data)
        data = self.normalize_invalid_values(data)
        data = self.normalize_missing_values(data)
        data = self.normalize_order(data)

        return data