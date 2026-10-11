from services.screening_service.app.api.schemas.screening_schema import (
    TrendScreeningConfig,
)


class TrendScreening:

    def screen(
        self,
        data: dict,
        config: TrendScreeningConfig,
    ) -> dict:
        results = {}

        if config.price_above_sma:
            results["price_above_sma"] = (
                data["price"] > data["sma_20"]
            )

        if config.price_above_ema:
            results["price_above_ema"] = (
                data["price"] > data["ema_20"]
            )

        if config.positive_momentum:
            results["positive_momentum"] = (
                data["momentum"] > 0
            )

        passed = all(results.values()) if results else True

        return {
            "passed": passed,
            "rules": results,
        }