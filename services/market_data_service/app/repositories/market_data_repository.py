from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import select

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

    def get_by_symbol( self, symbol: str) -> list[MarketData]:
        
        # Retrieve all stored records for the symbol.
        statement = (
            select(MarketData)
            .where(MarketData.symbol == symbol)
            .order_by(MarketData.datetime)
        )

        return self.session.execute(statement).scalars().all()