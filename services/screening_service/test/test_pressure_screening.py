from services.screening_service.app.api.schemas.screening_schema import (
    PressureScreeningConfig,
)
from services.screening_service.app.screening.pressure_screening import (
    PressureScreening,
)


def test_pressure_screening_passes():
    screening = PressureScreening()

    config = PressureScreeningConfig(
        min_buying_pressure=0.6,
        max_selling_pressure=0.4,
        buying_pressure_dominant=True,
    )

    data = {
        "buying_pressure": 0.7,
        "selling_pressure": 0.3,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is True
    assert all(result["rules"].values())


def test_pressure_screening_fails():
    screening = PressureScreening()

    config = PressureScreeningConfig(
        min_buying_pressure=0.7,
    )

    data = {
        "buying_pressure": 0.5,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is False
    assert result["rules"]["min_buying_pressure"] is False


def test_pressure_screening_skips_unrequested_rules():
    screening = PressureScreening()

    config = PressureScreeningConfig(
        buying_pressure_dominant=True,
    )

    data = {
        "buying_pressure": 0.7,
        "selling_pressure": 0.3,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert "buying_pressure_dominant" in result["rules"]
    assert "min_buying_pressure" not in result["rules"]
    assert "max_selling_pressure" not in result["rules"]