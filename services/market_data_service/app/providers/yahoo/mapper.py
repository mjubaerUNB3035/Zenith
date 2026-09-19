
import pandas as pd


class YahooMapper:

    def map_market_data(self, data):
        # Converts Yahoo Finance DataFrame data into InvestIQ market-data records.
        # data comes from YahooClient in app.providers.yahoo.client.
        # The returned records are passed to the validation layer.
        # This keeps Yahoo-specific DataFrame handling inside the Yahoo provider.
        if data is None or data.empty:
            return []

        records = []

        if isinstance(data.columns, pd.MultiIndex):

            for symbol in data.columns.get_level_values(0).unique():
                # Selects the OHLCV data belonging to one Yahoo ticker.
                # The symbol comes from Yahoo's MultiIndex column structure.
                symbol_data = data[symbol].copy()

                symbol_data = symbol_data.reset_index()

                for _, row in symbol_data.iterrows():
                    # Converts one Yahoo price row into one standard InvestIQ record.
                    # Values come directly from the selected Yahoo DataFrame row.
                    records.append(
                        {
                            "symbol": symbol,
                            "datetime": row["Datetime"],
                            "open": row["Open"],
                            "high": row["High"],
                            "low": row["Low"],
                            "close": row["Close"],
                            "volume": row["Volume"],
                        }
                    )

        else:
            # Handles the single-symbol DataFrame format returned by Yahoo.
            # The symbol must be supplied by the caller when Yahoo returns
            # a non-MultiIndex DataFrame.
            data = data.reset_index()

            for _, row in data.iterrows():
                # Converts one single-symbol Yahoo row into a standard record.
                # The OHLCV values come from the current Yahoo DataFrame row.
                records.append(
                    {
                        "datetime": row["Datetime"],
                        "open": row["Open"],
                        "high": row["High"],
                        "low": row["Low"],
                        "close": row["Close"],
                        "volume": row["Volume"],
                    }
                )

        return records