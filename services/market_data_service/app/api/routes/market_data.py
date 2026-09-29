
import pandas as pd

from fastapi import APIRouter

from services.market_data_service.app.clients.security_client import (
    SecurityClient,
)
from services.market_data_service.app.ingestion.batch_manager import (
    BatchManager,
)
from services.market_data_service.app.ingestion.bulk_ingestor import (
    BulkIngestor,
)
from shared.providers.yahoo.client import YahooClient
from shared.providers.yahoo.mapper import YahooMapper
from services.market_data_service.app.processing.market_data_processor import (
    MarketDataProcessor,
)
from services.market_data_service.app.normalization.market_data_normalizer import (
    MarketDataNormalizer,
)
from services.market_data_service.app.database.database import SessionLocal
from services.market_data_service.app.repositories.market_data_repository import (
    MarketDataRepository,
)


router = APIRouter(
    prefix="/market-data",
    tags=["Market Data"],
)


def create_batch_manager():
    # Creates the Market Data ingestion pipeline.
    # YahooClient retrieves market data.
    # YahooMapper converts Yahoo data into Zenith records.
    # BulkIngestor connects the provider and mapper.
    # BatchManager divides large symbol lists into batches.

    yahoo_client = YahooClient()
    yahoo_mapper = YahooMapper()

    ingestor = BulkIngestor(
        provider=yahoo_client,
        mapper=yahoo_mapper,
    )

    return BatchManager(
        ingestor=ingestor,
        batch_size=100,
    )


@router.get("/")
def get_market_data(
    symbols: str,
    period: str = "5d",
    interval: str = "1h",
):
    # Convert the comma-separated symbols from the request
    # into a clean list such as ["AAPL", "MSFT"].

    symbol_list = [
        symbol.strip().upper()
        for symbol in symbols.split(",")
        if symbol.strip()
    ]

    # Connect to the separate Security Service.
    # The Security Service verifies that each requested symbol exists.
    # If a symbol does not exist, the Security Service obtains and stores it.
    # Market Data does not access the Security database directly.

    security_client = SecurityClient()

    for symbol in symbol_list:
        security_client.ensure_security(symbol)

    # Create the Market Data ingestion pipeline.

    batch_manager = create_batch_manager()

    # Retrieve market data from Yahoo in batches.

    batches = batch_manager.fetch_in_batches(
        symbols=symbol_list,
        period=period,
        interval=interval,
    )

    # Combine all batches into one list of market-data records.

    records = [
        record
        for batch in batches
        for record in batch
    ]

    # Convert the records into a DataFrame so the processing
    # and normalization layers can work with the data.

    data = pd.DataFrame(records)

    # Process calculated market-data values.

    processor = MarketDataProcessor()

    # Normalize column names and data types.

    normalizer = MarketDataNormalizer()

    processed_data = processor.process(data)

    normalized_data = normalizer.normalize(
        processed_data
    )

    # Open a Market Data database session.

    session = SessionLocal()

    try:
        # Create the Market Data repository.

        repository = MarketDataRepository(session)

        # Convert the DataFrame into dictionaries for database storage.

        records_to_save = normalized_data.to_dict(
            orient="records"
        )

        # Save the processed market data.

        repository.save_many(records_to_save)

    finally:
        # Always close the database session.

        session.close()

    # Return the processed and normalized market data to the API caller.

    return normalized_data.to_dict(
        orient="records"
    )


# Endpoint: Retrieve stored market data
@router.get("/stored")
def get_market_data_by_symbol(
    symbol: str,
):
    # Open a Market Data database session.

    session = SessionLocal()

    try:
        # Create the Market Data repository.

        repository = MarketDataRepository(session)

        # Retrieve stored records for the requested symbol.

        stored_records = repository.get_by_symbol(
            symbol=symbol.strip().upper()
        )

        return stored_records

    finally:
        # Always close the database session.

        session.close()
