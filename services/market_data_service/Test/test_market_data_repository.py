from datetime import datetime, timezone

from services.market_data_service.app.database.database import SessionLocal
from services.market_data_service.app.models.market_data_model import MarketData
from services.market_data_service.app.repositories.market_data_repository import (
    MarketDataRepository,
)


def test_save_many():
    session = SessionLocal()

    try:
        repository = MarketDataRepository(session)

        record = {
            "symbol": "TEST",
            "datetime": datetime.now(timezone.utc),
            "interval": "1h",
            "open": 100.0,
            "high": 105.0,
            "low": 99.0,
            "close": 103.0,
            "volume": 1000000,
        }

        repository.save_many([record])

        saved_record = (
            session.query(MarketData)
            .filter(MarketData.symbol == "TEST")
            .first()
        )

        assert saved_record is not None
        assert saved_record.symbol == "TEST"
        assert saved_record.close == 103.0

        session.delete(saved_record)
        session.commit()

    finally:
        session.close()


def test_get_by_symbol():
    session = SessionLocal()

    try:
        repository = MarketDataRepository(session)

        first_record = MarketData(
            symbol="TEST",
            datetime=datetime(
                2026,
                9,
                25,
                10,
                30,
                tzinfo=timezone.utc,
            ),
            interval="1h",
            open=100.0,
            high=105.0,
            low=99.0,
            close=103.0,
            volume=1000000,
        )

        second_record = MarketData(
            symbol="TEST",
            datetime=datetime(
                2026,
                9,
                25,
                11,
                30,
                tzinfo=timezone.utc,
            ),
            interval="1h",
            open=103.0,
            high=107.0,
            low=102.0,
            close=106.0,
            volume=1200000,
        )

        session.add_all([
            first_record,
            second_record,
        ])
        session.commit()

        records = repository.get_by_symbol("TEST")

        assert len(records) == 2
        assert records[0].symbol == "TEST"
        assert records[1].symbol == "TEST"
        assert records[0].datetime < records[1].datetime
        assert records[0].close == 103.0
        assert records[1].close == 106.0

        session.delete(first_record)
        session.delete(second_record)
        session.commit()

    finally:
        session.close()


def test_count_by_symbol():
    session = SessionLocal()

    try:
        repository = MarketDataRepository(session)

        first_record = MarketData(
            symbol="TEST",
            datetime=datetime(
                2026,
                9,
                25,
                12,
                30,
                tzinfo=timezone.utc,
            ),
            interval="1h",
            open=100.0,
            high=105.0,
            low=99.0,
            close=103.0,
            volume=1000000,
        )

        second_record = MarketData(
            symbol="TEST",
            datetime=datetime(
                2026,
                9,
                25,
                13,
                30,
                tzinfo=timezone.utc,
            ),
            interval="1h",
            open=103.0,
            high=107.0,
            low=102.0,
            close=106.0,
            volume=1200000,
        )

        session.add_all([
            first_record,
            second_record,
        ])
        session.commit()

        count = repository.count_by_symbol("TEST")

        assert count == 2

        session.delete(first_record)
        session.delete(second_record)
        session.commit()

    finally:
        session.close()