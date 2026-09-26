from sqlalchemy import UniqueConstraint

from services.market_data_service.app.models.market_data_model import MarketData


def test_market_data_table_name():
    assert MarketData.__tablename__ == "market_data"


def test_market_data_columns():
    columns = MarketData.__table__.columns

    expected_columns = {
        "id",
        "symbol",
        "datetime",
        "interval",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "price_change",
        "price_change_percent",
        "trading_range",
        "average_volume",
        "average_price",
        "relative_volume",
        "buying_pressure",
        "selling_pressure",
        "momentum",
        "volatility",
    }

    assert set(columns.keys()) == expected_columns


def test_market_data_unique_constraint():
    constraints = [
        constraint
        for constraint in MarketData.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    ]

    assert len(constraints) == 1

    constraint = constraints[0]

    assert constraint.name == "uq_market_data_symbol_datetime_interval"

    assert [
        column.name
        for column in constraint.columns
    ] == [
        "symbol",
        "datetime",
    ]