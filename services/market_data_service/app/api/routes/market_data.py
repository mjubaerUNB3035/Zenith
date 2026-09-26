
import pandas as pd

from fastapi import APIRouter

from services.market_data_service.app.ingestion.batch_manager import BatchManager
from services.market_data_service.app.ingestion.bulk_ingestor import BulkIngestor
from services.market_data_service.app.providers.yahoo.client import YahooClient
from services.market_data_service.app.providers.yahoo.mapper import YahooMapper
from services.market_data_service.app.processing.market_data_processor import MarketDataProcessor
from services.market_data_service.app.normalization.market_data_normalizer import MarketDataNormalizer
from services.market_data_service.app.database.database import SessionLocal
from services.market_data_service.app.repositories.market_data_repository import (
    MarketDataRepository,
)


router = APIRouter(
    prefix="/market-data",
    tags=["Market Data"],
)


def create_batch_manager():
    # Creates the Market Data ingestion pipeline used by the API route.
    # YahooClient retrieves data, YahooMapper converts it, and BulkIngestor connects them.
    # BatchManager controls how symbols are divided into batches.
    # This keeps pipeline construction separate from API request handling.
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
    # Receives market-data parameters and starts the ingestion pipeline.
    symbol_list = [
        symbol.strip().upper()
        for symbol in symbols.split(",")
        if symbol.strip()
    ]

    batch_manager = create_batch_manager()

    batches = batch_manager.fetch_in_batches(
        symbols=symbol_list,
        period=period,
        interval=interval,
    )

    records = [
        record
        for batch in batches
        for record in batch
    ]

    data = pd.DataFrame(records)

    processor = MarketDataProcessor()
    normalizer = MarketDataNormalizer()

    processed_data = processor.process(data)
    normalized_data = normalizer.normalize(processed_data)

    session = SessionLocal()

    try:
        repository = MarketDataRepository(session)

        records_to_save = normalized_data.to_dict(
            orient="records"
        )

        repository.save_many(records_to_save)

    finally:
        session.close()

    return normalized_data.to_dict(
        orient="records"
    )

# End Point : Fetch
@router.get("/stored")
def get_market_data_by_symbol(
    symbol: str,
):
    # Retrieves stored market data for a specific symbol from the database.
    session = SessionLocal()

    try:
        repository = MarketDataRepository(session)
        stored_records = repository.get_by_symbol(
            symbol=symbol.strip().upper()
        )

        return stored_records

    finally:
        session.close()