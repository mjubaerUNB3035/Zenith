from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from services.market_data_service.app.models.market_data_model import MarketData


class MarketDataRepository:

    def __init__(self, session: Session):
        # Store the database session.
        self.session = session

    def save_many(
        self,
        records: list[dict],
    ) -> None:
        # Stop if there are no records to save.
        if not records:
            return

        statement = insert(MarketData).values(records)

        update_values = {
            "open": statement.excluded.open,
            "high": statement.excluded.high,
            "low": statement.excluded.low,
            "close": statement.excluded.close,
            "volume": statement.excluded.volume,
            "interval": statement.excluded.interval,
            "price_change": statement.excluded.price_change,
            "price_change_percent": statement.excluded.price_change_percent,
            "trading_range": statement.excluded.trading_range,
            "average_volume": statement.excluded.average_volume,
            "average_price": statement.excluded.average_price,
            "relative_volume": statement.excluded.relative_volume,
            "buying_pressure": statement.excluded.buying_pressure,
            "selling_pressure": statement.excluded.selling_pressure,
            "momentum": statement.excluded.momentum,
            "volatility": statement.excluded.volatility,
        }

        statement = statement.on_conflict_do_update(
            constraint="uq_market_data_symbol",
            set_=update_values,
        )

        self.session.execute(statement)
        self.session.commit()



    def get_by_symbol(
        self,
        symbol: str,
        interval: str | None = None,
        limit: int | None = None,
    ) -> list[MarketData]:

        # Retrieve stored records for the symbol.
        statement = (
            select(MarketData)
            .where(MarketData.symbol == symbol)
        )

        # Filter records by interval when one is provided.
        if interval is not None:
            statement = statement.where(
                MarketData.interval == interval
            )

        statement = statement.order_by(
            MarketData.datetime.desc()
        )

        if limit is not None:
            statement = statement.limit(limit)

        records = self.session.execute(
            statement
        ).scalars().all()

        return list(reversed(records))

    def count_by_symbol(
        self,
        symbol: str,
    ) -> int:

        # Count how many records exist for the symbol.
        statement = (
            select(func.count())
            .select_from(MarketData)
            .where(MarketData.symbol == symbol)
        )

        return self.session.execute(statement).scalar_one()

    # Retrieve the latest market-data records when indicator triggers.
    def get_latest_market_data_for_indicator(
        self,
        symbol: str,
        interval: str,
        limit: int,
    ) -> list[MarketData]:

        # Retrieve the latest market-data records
        # for the requested symbol and interval.

        statement = (
            select(MarketData)
            .where(
                MarketData.symbol == symbol,
                MarketData.interval == interval,
            )
            .order_by(MarketData.datetime.desc())
            .limit(limit)
        )

        records = self.session.execute(
            statement
        ).scalars().all()

        # Reverse the records so the oldest requested candle
        # comes first and the newest candle comes last.

        return list(reversed(records))