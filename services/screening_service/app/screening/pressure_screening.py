from services.screening_service.app.api.schemas.screening_schema import (
    PressureScreeningConfig,
)


class PressureScreening:

    def screen(
        self,
        data: dict,
        config: PressureScreeningConfig,
    ) -> dict:
        results = {}

        if config.min_buying_pressure is not None:
            results["min_buying_pressure"] = (
                data["buying_pressure"]
                >= config.min_buying_pressure
            )

        if config.max_selling_pressure is not None:
            results["max_selling_pressure"] = (
                data["selling_pressure"]
                <= config.max_selling_pressure
            )

        if config.buying_pressure_dominant:
            results["buying_pressure_dominant"] = (
                data["buying_pressure"]
                > data["selling_pressure"]
            )

        passed = all(results.values()) if results else True

        return {
            "passed": passed,
            "rules": results,
        }