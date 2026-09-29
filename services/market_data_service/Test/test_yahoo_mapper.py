import pandas as pd
from shared.providers.yahoo.mapper import YahooMapper


def test_map_market_data():
    columns = pd.MultiIndex.from_tuples(
        [
            ("AAPL", "Open"),
            ("AAPL", "High"),
            ("AAPL", "Low"),
            ("AAPL", "Close"),
            ("AAPL", "Volume"),
        ]
    )

    data = pd.DataFrame(
        [
            [100.0, 105.0, 99.0, 103.0, 1000000],
        ],
        index=pd.DatetimeIndex(
            ["2026-09-12 10:00:00"],
            name="Datetime",
        ),
        columns=columns,
    )

    mapper = YahooMapper()

    records = mapper.map_market_data(
        data,
        interval="1h",
    )

    assert len(records) == 1
    assert records[0]["symbol"] == "AAPL"
    assert records[0]["interval"] == "1h"
    assert records[0]["open"] == 100.0
    assert records[0]["high"] == 105.0
    assert records[0]["low"] == 99.0
    assert records[0]["close"] == 103.0
    assert records[0]["volume"] == 1000000