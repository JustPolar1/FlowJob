from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.members import router as members_router
from app.db.database import Base, SessionLocal, engine
from app import models  # noqa: F401 — importing registers the service's models with Base.
from app.services.member_service import seed_default_members

app = FastAPI(
    title="FlowJob Member Service",
    description="Servicio responsable de la gestión de integrantes.",
    version="0.1.0",
)

app.include_router(health_router, tags=["health"])
app.include_router(members_router)


@app.on_event("startup")
def create_member_tables() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_default_members(db)
