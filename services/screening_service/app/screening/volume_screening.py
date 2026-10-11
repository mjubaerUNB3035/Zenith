from services.screening_service.app.api.schemas.screening_schema import (
    VolumeScreeningConfig,
)


class VolumeScreening:

    def screen(
        self,
        data: dict,
        config: VolumeScreeningConfig,
    ) -> dict:
        results = {}

        if config.min_relative_volume is not None:
            results["min_relative_volume"] = (
                data["relative_volume"]
                >= config.min_relative_volume
            )

        if config.volume_above_average:
            results["volume_above_average"] = (
                data["volume"] > data["average_volume"]
            )

        passed = all(results.values()) if results else True

        return {
            "passed": passed,
            "rules": results,
        }