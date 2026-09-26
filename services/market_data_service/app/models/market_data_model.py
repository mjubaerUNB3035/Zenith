from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MarketData(Base):
    __tablename__ = "market_data"

    __table_args__ = (
        UniqueConstraint(
            "symbol",
            "datetime",
            name="uq_market_data_symbol_datetime_interval",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    interval: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    open: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    high: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    low: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    close: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    volume: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    price_change: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    price_change_percent: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    trading_range: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    average_volume: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    average_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    relative_volume: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    buying_pressure: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    selling_pressure: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    momentum: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    volatility: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )