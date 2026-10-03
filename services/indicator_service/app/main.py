from fastapi import FastAPI
from services.indicator_service.app.api.routes.indicator_routes import (
    router,
)

app = FastAPI(
    title="Zenith Indicator Service",
    description="Calculates technical indicators from market data.",
    version="1.0.0",
)

app.include_router(router)