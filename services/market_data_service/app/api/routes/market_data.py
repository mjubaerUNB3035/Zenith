import pandas as pd

from fastapi import APIRouter

from services.market_data_service.app.ingestion.batch_manager import BatchManager
from services.market_data_service.app.ingestion.bulk_ingestor import BulkIngestor
from services.market_data_service.app.providers.yahoo.client import YahooClient
from services.market_data_service.app.providers.yahoo.mapper import YahooMapper
from services.market_data_service.app.processing.market_data_processor import MarketDataProcessor
from services.market_data_service.app.normalization.market_data_normalizer import MarketDataNormalizer

router = APIRouter(
    prefix="/market-data",2r
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

    return normalized_data.to_dict(orient="records")