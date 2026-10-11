from services.screening_service.app.api.schemas.screening_schema import (
    BasicScreeningConfig,
)


class BasicScreening:

    def screen(
        self,
        data: dict,
        config: BasicScreeningConfig,
    ) -> dict:
        results = {}

        if config.min_price is not None:
            results["min_price"] = (
                data["price"] >= config.min_price
            )

        if config.max_price is not None:
            results["max_price"] = (
                data["price"] <= config.max_price
            )

        if config.min_volume is not None:
            results["min_volume"] = (
                data["volume"] >= config.min_volume
            )

        if config.min_relative_volume is not None:
            results["min_relative_volume"] = (
                data["relative_volume"]
                >= config.min_relative_volume
            )

        if config.min_momentum is not None:
            results["min_momentum"] = (
                data["momentum"]
                >= config.min_momentum
            )

        if config.min_volatility is not None:
            results["min_volatility"] = (
                data["volatility"]
                >= config.min_volatility
            )

        passed = all(results.values()) if results else True

        return {
            "passed": passed,
            "rules": results,
        }