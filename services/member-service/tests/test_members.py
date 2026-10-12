from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    def override_get_db() -> Generator[Session, None, None]:
        db = test_session_local()
        try:
            yield db
        finally:
            db.close()

    monkeypatch.setitem(app.dependency_overrides, get_db, override_get_db)
    try:
        yield TestClient(app)
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_register_member_trims_name_and_returns_created_member(
    client: TestClient,
) -> None:
    response = client.post("/members", json={"name": "  Ada Lovelace  "})

    assert response.status_code == 201
    assert response.json()["name"] == "Ada Lovelace"
    assert response.json()["id"] > 0


def test_list_members_returns_members_in_id_order(client: TestClient) -> None:
    first = client.post("/members", json={"name": "Ada Lovelace"}).json()
    second = client.post("/members", json={"name": "Grace Hopper"}).json()

    response = client.get("/members")

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_read_member_returns_member_by_id(client: TestClient) -> None:
    created = client.post("/members", json={"name": "Ada Lovelace"}).json()

    response = client.get(f"/members/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_read_member_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get("/members/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Integrante no encontrado"


@pytest.mark.parametrize("name", ["", "   ", "A" * 121])
def test_register_member_rejects_invalid_name(
    client: TestClient,
    name: str,
) -> None:
    response = client.post("/members", json={"name": name})

    assert response.status_code == 422
