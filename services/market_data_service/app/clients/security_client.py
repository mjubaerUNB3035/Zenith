
import requests


class SecurityClient:

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8001",
    ):
        # URL of the separate Security Service.
        self.base_url = base_url

    def ensure_security(self, symbol: str):
        # Connects to the Security Service and asks it
        # to find or create the requested security.

        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError("A symbol is required.")

        response = requests.get(
            f"{self.base_url}/securities/ensure/{symbol}",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()
