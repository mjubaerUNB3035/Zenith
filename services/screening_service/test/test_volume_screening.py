from services.screening_service.app.api.schemas.screening_schema import (
    VolumeScreeningConfig,
)
from services.screening_service.app.screening.volume_screening import (
    VolumeScreening,
)


def test_volume_screening_passes():
    screening = VolumeScreening()

    config = VolumeScreeningConfig(
        min_relative_volume=1.5,
        volume_above_average=True,
    )

    data = {
        "relative_volume": 2.0,
        "volume": 2000000,
        "average_volume": 1500000,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is True
    assert all(result["rules"].values())


def test_volume_screening_fails():
    screening = VolumeScreening()

    config = VolumeScreeningConfig(
        min_relative_volume=2.0,
    )

    data = {
        "relative_volume": 1.5,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert result["passed"] is False
    assert result["rules"]["min_relative_volume"] is False


def test_volume_screening_skips_unrequested_rules():
    screening = VolumeScreening()

    config = VolumeScreeningConfig(
        volume_above_average=True,
    )

    data = {
        "volume": 2000000,
        "average_volume": 1500000,
    }

    result = screening.screen(
        data=data,
        config=config,
    )

    assert "volume_above_average" in result["rules"]
    assert "min_relative_volume" not in result["rules"]