from services.screening_service.app.api.schemas.screening_schema import (
    MomentumScreeningConfig,
)
from services.screening_service.app.screening.momentum_screening import (
    MomentumScreening,
)


def test_momentum_screening_passes():
    screening = MomentumScreening()

    config = MomentumScreeningConfig(
        min_rsi=50,
        max_rsi=70,
        positive_momentum=True,
        min_relative_volume=1.5,
    )

    data = {
        "rsi_14": 60,
        "momentum": 5,
        "relative_volume": 2.0,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is True
    assert all(result["rules"].values())


def test_momentum_screening_fails():
    screening = MomentumScreening()

    config = MomentumScreeningConfig(
        min_rsi=70,
    )

    data = {
        "rsi_14": 60,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is False
    assert result["rules"]["min_rsi"] is False


def test_momentum_screening_skips_unrequested_rules():
    screening = MomentumScreening()

    config = MomentumScreeningConfig(
        positive_momentum=True,
    )

    data = {
        "momentum": 5,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert "positive_momentum" in result["rules"]
    assert "min_rsi" not in result["rules"]
    assert "max_rsi" not in result["rules"]
    assert "min_relative_volume" not in result["rules"]