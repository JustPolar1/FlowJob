import pytest
from fastapi.testclient import TestClient

from app.clients import member_client
import app.services.task_service as task_service
from app.main import app
from app.clients.member_client import MemberServiceUnavailableError
from app.repositories.task_repository import TaskRepository


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(member_client, "member_exists", lambda member_id: True)
    monkeypatch.setattr(task_service, "repository", TaskRepository())
    return TestClient(app)


def test_create_task_accepts_assignee_id(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Preparar informe", "assignee_id": 17},
    )

    assert response.status_code == 201
    assert response.json()["assignee_id"] == 17


def test_update_task_assigns_assignee_id(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Preparar informe"})
    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"assignee_id": 17},
    )

    assert response.status_code == 200
    assert response.json()["assignee_id"] == 17


def test_create_task_rejects_unknown_assignee(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(member_client, "member_exists", lambda member_id: False)

    response = client.post(
        "/tasks",
        json={"title": "Preparar informe", "assignee_id": 999},
    )

    assert response.status_code == 422
    assert client.get("/tasks").json() == []


def test_update_task_rejects_unknown_assignee(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created = client.post("/tasks", json={"title": "Preparar informe"}).json()
    monkeypatch.setattr(member_client, "member_exists", lambda member_id: False)

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"assignee_id": 999},
    )

    assert response.status_code == 422
    assert client.get(f"/tasks/{created['id']}").json()["assignee_id"] is None


def test_create_task_returns_503_when_member_service_is_unavailable(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_unavailable(member_id: int) -> bool:
        raise MemberServiceUnavailableError(
            "No se pudo consultar el servicio de integrantes."
        )

    monkeypatch.setattr(member_client, "member_exists", raise_unavailable)

    response = client.post(
        "/tasks",
        json={"title": "Preparar informe", "assignee_id": 17},
    )

    assert response.status_code == 503
    assert client.get("/tasks").json() == []


def test_update_task_returns_503_when_member_service_is_unavailable(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created = client.post("/tasks", json={"title": "Preparar informe"}).json()

    def raise_unavailable(member_id: int) -> bool:
        raise MemberServiceUnavailableError(
            "No se pudo consultar el servicio de integrantes."
        )

    monkeypatch.setattr(member_client, "member_exists", raise_unavailable)

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"assignee_id": 17},
    )

    assert response.status_code == 503
    assert client.get(f"/tasks/{created['id']}").json()["assignee_id"] is None
