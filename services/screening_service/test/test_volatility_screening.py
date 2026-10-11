from services.screening_service.app.api.schemas.screening_schema import (
    VolatilityScreeningConfig,
)
from services.screening_service.app.screening.volatility_screening import (
    VolatilityScreening,
)


def test_volatility_screening_passes():
    screening = VolatilityScreening()

    config = VolatilityScreeningConfig(
        min_volatility=0.01,
        max_volatility=0.05,
    )

    data = {
        "volatility": 0.025,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is True
    assert all(result["rules"].values())


def test_volatility_screening_fails():
    screening = VolatilityScreening()

    config = VolatilityScreeningConfig(
        min_volatility=0.03,
    )

    data = {
        "volatility": 0.02,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is False
    assert result["rules"]["min_volatility"] is False


def test_volatility_screening_skips_unrequested_rules():
    screening = VolatilityScreening()

    config = VolatilityScreeningConfig(
        max_volatility=0.05,
    )

    data = {
        "volatility": 0.025,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert "max_volatility" in result["rules"]
    assert "min_volatility" not in result["rules"]