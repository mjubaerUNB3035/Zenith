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


# Fresh Data for and

def refresh_and_get_market_data_for_indicator(
    symbol: str,
    required_candles: int,
):
    # Connect to the separate Security Service.
    # The Security Service verifies that the requested symbol exists.
    # If the symbol does not exist, the Security Service obtains and stores it.

    security_client = SecurityClient()

    security_client.ensure_security(symbol)

    # Retrieve fresh daily market data from Yahoo.
    # This refresh happens when the Indicator requests market data.

    yahoo_client = YahooClient()
    yahoo_mapper = YahooMapper()

    market_data = yahoo_client.get_market_data(
        symbols=[symbol],
        period="1y",
        interval="1d",
    )

    # Convert Yahoo data into Zenith market-data records.

    records = yahoo_mapper.map_market_data(
        market_data,
        interval="1d",
    )

    # Convert the records into a DataFrame.

    data = pd.DataFrame(records)

    # Process calculated market-data values.

    processor = MarketDataProcessor()

    processed_data = processor.process(data)

    # Normalize column names and data types.

    normalizer = MarketDataNormalizer()

    normalized_data = normalizer.normalize(
        processed_data
    )

    # Open a Market Data database session.

    session = SessionLocal()

    try:
        # Create the Market Data repository.

        repository = MarketDataRepository(session)

        # Convert the processed data into dictionaries
        # for database storage.

        records_to_save = normalized_data.to_dict(
            orient="records"
        )

        # Store the fresh market data.

        repository.save_many(records_to_save)

        # Retrieve the latest required number of daily candles.

        stored_records = repository.get_latest_market_data_for_indicator(
            symbol=symbol,
            interval="1d",
            limit=required_candles,
        )

        return stored_records

    finally:
        # Always close the database session.

        session.close()


# Endpoint: Retrieve fresh market data for the Indicator Service

@router.get("/for-indicator")
def get_market_data_for_indicator(
    symbol: str,
    required_candles: int = 200,
):
    # Retrieve fresh market data and return
    # the latest candles required by the Indicator Service.

    return refresh_and_get_market_data_for_indicator(
        symbol=symbol.strip().upper(),
        required_candles=required_candles,
    )


@router.post("/ingest")
def ingest_market_data(
    symbols: str,
    minimum_candles: int = 200,
    interval: str = "1d",
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

    period = "1y"

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

    for symbol in symbol_list:
        symbol_records = [
            record
            for record in records
            if record["symbol"] == symbol
        ]

        if len(symbol_records) < minimum_candles:
            raise ValueError(
                f"Not enough market data returned for {symbol}. "
                f"Required: {minimum_candles}, "
                f"Received: {len(symbol_records)}."
            )

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
    interval: str | None = None,
    limit: int | None = None,
):
    # Open a Market Data database session.

    session = SessionLocal()

    try:
        # Create the Market Data repository.

        repository = MarketDataRepository(session)

        # Retrieve stored records for the requested symbol.

        stored_records = repository.get_by_symbol(
            symbol=symbol.strip().upper(),
            interval=interval,
            limit=limit,
        )

        return stored_records

    finally:
        # Always close the database session.

        session.close()