from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.members import router as members_router
from app.api.routes.tasks import router as tasks_router
from app.core.config import settings

app = FastAPI(
    title="FlowJob API Gateway",
    description="Punto de entrada para los servicios de FlowJob.",
    version="0.1.0",
)

app.include_router(health_router, tags=["health"])
app.include_router(tasks_router, prefix=settings.api_prefix, tags=["tasks"])
app.include_router(members_router, prefix=settings.api_prefix, tags=["members"])
