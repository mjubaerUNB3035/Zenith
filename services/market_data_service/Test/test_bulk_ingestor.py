import pandas as pd

from services.market_data_service.app.ingestion.bulk_ingestor import BulkIngestor
from services.market_data_service.app.providers.yahoo.mapper import YahooMapper


class FakeProvider:

    def get_market_data(self, symbols, period, interval):
        columns = pd.MultiIndex.from_tuples(
            [
                ("AAPL", "Open"),
                ("AAPL", "High"),
                ("AAPL", "Low"),
                ("AAPL", "Close"),
                ("AAPL", "Volume"),
                ("MSFT", "Open"),
                ("MSFT", "High"),
                ("MSFT", "Low"),
                ("MSFT", "Close"),
                ("MSFT", "Volume"),
                ("NVDA", "Open"),
                ("NVDA", "High"),
                ("NVDA", "Low"),
                ("NVDA", "Close"),
                ("NVDA", "Volume"),
            ]
        )

        return pd.DataFrame(
            [
                [
                    100, 103, 99, 102, 1000,
                    200, 203, 199, 202, 2000,
                    300, 303, 299, 302, 3000,
                ]
            ],
            index=pd.DatetimeIndex(
                ["2026-09-12"],
                name="Datetime",
            ),
            columns=columns,
        )


def test_bulk_ingestor_fetches_multiple_symbols():
    provider = FakeProvider()
    mapper = YahooMapper()

    ingestor = BulkIngestor(provider, mapper)

    result = ingestor.fetch(
        symbols=["AAPL", "MSFT", "NVDA"],
        period="5d",
        interval="1h",
    )

    assert len(result) == 3
    assert result[0]["symbol"] == "AAPL"
    assert result[1]["symbol"] == "MSFT"
    assert result[2]["symbol"] == "NVDA"


def test_bulk_ingestor_rejects_empty_symbols():
    provider = FakeProvider()
    mapper = YahooMapper()

    ingestor = BulkIngestor(provider, mapper)

    try:
        ingestor.fetch([])
        assert False
    except ValueError as exc:
        assert str(exc) == "At least one symbol is required."