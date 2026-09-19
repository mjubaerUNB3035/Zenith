import yfinance as yf


class YahooClient:

    def get_market_data(self, symbols, period="5d", interval="1h"):
        # Fetches market data for multiple symbols from Yahoo Finance.
        # symbols, period, and interval come from the ingestion layer.
        # This method is called by BulkIngestor through the provider connection.
        # yfinance is the external dependency used only inside the Yahoo provider.
        # The returned data remains Yahoo/provider data and is not processed here.
        if not symbols:
            raise ValueError("At least one symbol is required.")

        return yf.download(
            tickers=symbols,
            period=period,
            interval=interval,
            group_by="ticker",
            auto_adjust=False,
            progress=False,
        )