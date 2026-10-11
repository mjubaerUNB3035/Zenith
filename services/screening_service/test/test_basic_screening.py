from services.screening_service.app.api.schemas.screening_schema import (
    BasicScreeningConfig,
)
from services.screening_service.app.screening.basic_screening import (
    BasicScreening,
)


def test_basic_screening_passes():
    screening = BasicScreening()

    config = BasicScreeningConfig(
        min_price=50,
        min_volume=1000000,
        min_relative_volume=1.5,
        min_momentum=0,
        min_volatility=0.01,
    )

    data = {
        "price": 100,
        "volume": 2000000,
        "relative_volume": 2.0,
        "momentum": 5.0,
        "volatility": 0.02,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is True
    assert all(result["rules"].values())


def test_basic_screening_fails_price():
    screening = BasicScreening()

    config = BasicScreeningConfig(
        min_price=150,
    )

    data = {
        "price": 100,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is False
    assert result["rules"]["min_price"] is False


def test_basic_screening_skips_unrequested_rules():
    screening = BasicScreening()

    config = BasicScreeningConfig(
        min_price=50,
    )

    data = {
        "price": 100,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert "min_price" in result["rules"]
    assert "min_volume" not in result["rules"]
    assert "min_relative_volume" not in result["rules"]
    assert "min_momentum" not in result["rules"]
    assert "min_volatility" not in result["rules"]