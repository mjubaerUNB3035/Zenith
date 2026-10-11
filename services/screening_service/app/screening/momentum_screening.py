from services.screening_service.app.api.schemas.screening_schema import (
    MomentumScreeningConfig,
)


class MomentumScreening:

    def screen(
        self,
        data: dict,
        config: MomentumScreeningConfig,
    ) -> dict:
        results = {}

        if config.min_rsi is not None:
            results["min_rsi"] = (
                data["rsi_14"] >= config.min_rsi
            )

        if config.max_rsi is not None:
            results["max_rsi"] = (
                data["rsi_14"] <= config.max_rsi
            )

        if config.positive_momentum:
            results["positive_momentum"] = (
                data["momentum"] > 0
            )

        if config.min_relative_volume is not None:
            results["min_relative_volume"] = (
                data["relative_volume"]
                >= config.min_relative_volume
            )

        passed = all(results.values()) if results else True

        return {
            "passed": passed,
            "rules": results,
        }