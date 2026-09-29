from shared.providers.yahoo.client import YahooClient

from services.security_service.app.models.security_model import Security
from services.security_service.app.repositories.security_repository import (
    SecurityRepository,
)


class SecurityIngestor:

    def __init__(self, repository: SecurityRepository):
        # Repository handles retrieving and saving Security records.
        self.repository = repository

        # YahooClient retrieves security information from Yahoo Finance.
        self.yahoo_client = YahooClient()

    def ingest(self, symbol: str):
        # Clean the symbol before using it.
        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError("A symbol is required.")

        # First check whether the security already exists.
        existing_security = self.repository.get_by_symbol(
            symbol
        )

        if existing_security:
            return existing_security

        # Security does not exist, so retrieve its information from Yahoo.
        security_data = self.yahoo_client.get_security_info(
            symbol
        )

        if not security_data:
            raise ValueError(
                f"No security information found for symbol: {symbol}"
            )

        # Yahoo returns a dictionary.
        # Convert that dictionary into our SQLAlchemy Security model.
        security = Security(
            symbol=security_data["symbol"],
            company_name=security_data["company_name"],
            exchange=security_data.get("exchange"),
            sector=security_data.get("sector"),
            industry=security_data.get("industry"),
            country=security_data.get("country"),
            active=security_data.get("active", True),
        )

        # The repository expects a Security model,
        # so we pass the converted object here.
        return self.repository.create(security)