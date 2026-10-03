import requests


class MarketDataClient:

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
    ):
        self.base_url = base_url

    def get_market_data_for_indicator(
        self,
        symbol: str,
        required_candles: int = 200,
    ):
        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError("A symbol is required.")

        response = requests.get(
            f"{self.base_url}/market-data/for-indicator",
            params={
                "symbol": symbol,
                "required_candles": required_candles,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()