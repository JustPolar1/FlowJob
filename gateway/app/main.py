from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(
    title="FlowJob API Gateway",
    description="Punto de entrada para los servicios de FlowJob.",
    version="0.1.0",
)

app.include_router(health_router, tags=["health"])
