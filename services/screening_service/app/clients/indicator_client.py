import requests


class IndicatorClient:

    #Define the url
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8002",
    ):
        self.base_url = base_url

    #Indicators metod
    def get_indicators(
        self,
        symbol: str,
        candles: int,
    ):
        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError("A symbol is required.")

        if candles <= 0:
            raise ValueError(
                "Candles must be greater than zero."
            )

        response = requests.get(
            f"{self.base_url}/indicators/{symbol}",
            params={
                "candles": candles,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()