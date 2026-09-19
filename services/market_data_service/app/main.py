from fastapi import FastAPI

from services.market_data_service.app.api.routes.market_data import router as market_data_router


app = FastAPI(
    title="InvestIQ Market Data Service",
    version="1.0.0",
)

app.include_router(market_data_router)