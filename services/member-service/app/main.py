from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(
    title="FlowJob Member Service",
    description="Servicio responsable de la gestión de integrantes.",
    version="0.1.0",
)

app.include_router(health_router, tags=["health"])
