from unittest.mock import patch

from fastapi.testclient import TestClient

from services.security_service.app.main import app


client = TestClient(app)


def test_ensure_security():
    # Tests that the ensure endpoint returns security information
    # provided by the SecurityIngestor.
    security_data = {
        "id": 1,
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "exchange": "NMS",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "United States",
        "active": True,
    }

    with patch(
        "services.security_service.app.api.routes.security_routes.SecurityIngestor"
    ) as mock_ingestor:

        mock_ingestor.return_value.ingest.return_value = security_data

        response = client.get("/securities/ensure/AAPL")

    assert response.status_code == 200
    assert response.json() == security_data

    mock_ingestor.return_value.ingest.assert_called_once_with("AAPL")