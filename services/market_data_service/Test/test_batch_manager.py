
from services.market_data_service.app.ingestion.batch_manager import BatchManager
from services.market_data_service.app.ingestion.bulk_ingestor import BulkIngestor
from services.market_data_service.app.providers.yahoo.client import YahooClient
from services.market_data_service.app.providers.yahoo.mapper import YahooMapper


class TestProvider:

    def get_market_data(self, symbols, period, interval):
        # Provides controlled test data to BatchManager through BulkIngestor.
        # In production, this dependency is replaced by YahooClient.
        return {
            "symbols": symbols,
            "period": period,
            "interval": interval,
        }


class TestMapper:

    def map_market_data(self, data):
        # Provides a controlled mapper for testing BatchManager's batching behavior.
        # In production, this dependency is replaced by YahooMapper.
        return data


def test_batch_manager_calls_ingestor_for_each_batch():
    # Tests that BatchManager splits symbols into batches and calls BulkIngestor.
    # TestProvider and TestMapper keep this test focused only on batching behavior.
    provider = TestProvider()
    mapper = TestMapper()
    ingestor = BulkIngestor(provider, mapper)
    manager = BatchManager(ingestor, batch_size=2)

    result = manager.fetch_in_batches(
        symbols=["AAPL", "MSFT", "NVDA", "AMZN", "META"],
        period="5d",
        interval="1h",
    )

    assert len(result) == 3
    assert result[0]["symbols"] == ["AAPL", "MSFT"]
    assert result[1]["symbols"] == ["NVDA", "AMZN"]
    assert result[2]["symbols"] == ["META"]


def test_batch_manager_rejects_empty_symbols():
    # Tests that BatchManager rejects an empty symbol list before calling BulkIngestor.
    # The test dependencies are not used when the input is invalid.
    provider = TestProvider()
    mapper = TestMapper()
    ingestor = BulkIngestor(provider, mapper)
    manager = BatchManager(ingestor, batch_size=2)

    try:
        manager.fetch_in_batches([])
        assert False
    except ValueError as exc:
        assert str(exc) == "At least one symbol is required."


def test_batch_manager_uses_yahoo_mapper():
    # Tests the real BatchManager -> BulkIngestor -> YahooClient -> YahooMapper connection.
    # YahooClient retrieves provider data and YahooMapper converts it into InvestIQ records.
    yahoo_client = YahooClient()
    yahoo_mapper = YahooMapper()

    ingestor = BulkIngestor(
        provider=yahoo_client,
        mapper=yahoo_mapper,
    )

    manager = BatchManager(
        ingestor=ingestor,
        batch_size=2,
    )

    result = manager.fetch_in_batches(
        symbols=["AAPL", "MSFT"],
        period="5d",
        interval="1h",
    )

    assert len(result) == 1
    assert result[0]
    assert all("symbol" in record for record in result[0])
    assert all("datetime" in record for record in result[0])
    assert all("open" in record for record in result[0])
    assert all("high" in record for record in result[0])
    assert all("low" in record for record in result[0])
    assert all("close" in record for record in result[0])
    assert all("volume" in record for record in result[0])