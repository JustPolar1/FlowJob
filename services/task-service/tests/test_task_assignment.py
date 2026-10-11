import pytest
from fastapi.testclient import TestClient

import app.services.task_service as task_service
from app.main import app
from app.repositories.task_repository import TaskRepository


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
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
