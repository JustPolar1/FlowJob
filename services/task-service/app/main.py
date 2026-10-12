from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as tasks_router
from app.db.database import Base, engine
from app import models  # noqa: F401 — importing registers the service's models with Base.

app = FastAPI(
    title="FlowJob Task Service",
    description="API para consultar y administrar tareas del equipo.",
    version="0.1.0",
)

app.include_router(health_router, tags=["health"])
app.include_router(tasks_router, tags=["tasks"])


@app.on_event("startup")
def create_task_tables() -> None:
    Base.metadata.create_all(bind=engine)
