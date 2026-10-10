from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.db.database import Base, engine
from app import models  # noqa: F401 — importing registers the service's models with Base.

app = FastAPI(
    title="FlowJob Task Service",
    description="Servicio responsable de la gestión de tareas.",
    version="0.1.0",
)

app.include_router(health_router, tags=["health"])


@app.on_event("startup")
def create_task_tables() -> None:
    Base.metadata.create_all(bind=engine)
