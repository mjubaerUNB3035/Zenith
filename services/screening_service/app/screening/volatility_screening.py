from services.screening_service.app.api.schemas.screening_schema import (
    VolatilityScreeningConfig,
)


class VolatilityScreening:

    def screen(
        self,
        data: dict,
        config: VolatilityScreeningConfig,
    ) -> dict:
        results = {}

        if config.min_volatility is not None:
            results["min_volatility"] = (
                data["volatility"]
                >= config.min_volatility
            )

        if config.max_volatility is not None:
            results["max_volatility"] = (
                data["volatility"]
                <= config.max_volatility
            )

        passed = all(results.values()) if results else True

        return {
            "passed": passed,
            "rules": results,
        }