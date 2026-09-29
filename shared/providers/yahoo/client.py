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

    def get_security_info(self, symbol: str):
        # Gets company/security information for one symbol from Yahoo Finance.
        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError("A symbol is required.")

        ticker = yf.Ticker(symbol)

        info = ticker.info

        if not info:
            return None

        return {
            "symbol": symbol,
            "company_name": info.get("longName") or info.get("shortName"),
            "exchange": info.get("exchange"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "active": True,
        }