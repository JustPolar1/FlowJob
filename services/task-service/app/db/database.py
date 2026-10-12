import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


SERVICE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = SERVICE_ROOT / "data" / "tasks.db"
DATABASE_URL = os.getenv("TASK_DATABASE_URL", f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}")

if DATABASE_URL.startswith("sqlite:///") and ":memory:" not in DATABASE_URL:
    database_path = Path(DATABASE_URL.removeprefix("sqlite:///"))
    database_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
