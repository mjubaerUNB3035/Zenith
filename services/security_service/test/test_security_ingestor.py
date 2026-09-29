from unittest.mock import Mock

from services.security_service.app.models.security_model import Security
from services.security_service.app.ingestion.security_ingestor import (
    SecurityIngestor,
)
def test_security_ingestor_creates_missing_security():
    # Tests that a missing security is retrieved from Yahoo
    # and converted into a Security model before being saved.

    repository = Mock()
    yahoo_client = Mock()

    repository.get_by_symbol.return_value = None

    security_data = {
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "exchange": "NMS",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "United States",
        "active": True,
    }

    yahoo_client.get_security_info.return_value = security_data

    security_model = Security(
        symbol="AAPL",
        company_name="Apple Inc.",
        exchange="NMS",
        sector="Technology",
        industry="Consumer Electronics",
        country="United States",
        active=True,
    )

    repository.create.return_value = security_model

    ingestor = SecurityIngestor(repository)

    # Replace the real Yahoo client with our mocked client.
    ingestor.yahoo_client = yahoo_client

    result = ingestor.ingest("aapl")

    assert result == security_model

    repository.get_by_symbol.assert_called_once_with("AAPL")

    yahoo_client.get_security_info.assert_called_once_with("AAPL")

    # Verify that the repository received a Security model.
    created_security = repository.create.call_args[0][0]

    assert isinstance(created_security, Security)
    assert created_security.symbol == "AAPL"
    assert created_security.company_name == "Apple Inc."
    assert created_security.exchange == "NMS"
    assert created_security.sector == "Technology"
    assert created_security.industry == "Consumer Electronics"
    assert created_security.country == "United States"
    assert created_security.active is True