from fastapi import FastAPI

from services.security_service.app.api.routes.security_routes import router


app = FastAPI(
    title="Zenith Security Service",
)


app.include_router(router)