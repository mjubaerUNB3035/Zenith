from services.market_data_service.app.clients.security_client import (
    SecurityClient,
)


def test_ensure_security():
    client = SecurityClient()

    result = client.ensure_security("AAPL")

    assert result["symbol"] == "AAPL"
    assert result["company_name"] == "Apple Inc."