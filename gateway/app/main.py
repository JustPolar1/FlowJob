from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.root import router as root_router
from app.core.config import settings

app = FastAPI(
    title="FlowJob API Gateway",
    description="Punto de entrada para los servicios de FlowJob.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(health_router, tags=["health"])
app.include_router(root_router, prefix=settings.api_prefix, tags=["api"])
