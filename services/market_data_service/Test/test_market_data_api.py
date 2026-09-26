from fastapi.testclient import TestClient

from services.api_gateway.app.main import app


client = TestClient(app)


def test_get_market_data_by_symbol():
    response = client.get(
        "/market-data/stored",
        params={"symbol": "TSLA"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    assert data[0]["symbol"] == "TSLA"