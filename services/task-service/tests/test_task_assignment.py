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


def test_get_task_returns_created_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Preparar informe"}).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["title"] == "Preparar informe"


def test_get_task_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get("/tasks/999")

    assert response.status_code == 404


def test_delete_task_removes_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Preparar informe"}).json()

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.delete("/tasks/999")

    assert response.status_code == 404


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


def test_list_tasks_filters_by_status(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Pendiente", "status": "Pendiente"})
    client.post("/tasks", json={"title": "En proceso", "status": "En proceso"})

    response = client.get("/tasks", params={"status": "Pendiente"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Pendiente"]


def test_list_tasks_filters_by_assignee(client: TestClient) -> None:
    client.post(
        "/tasks",
        json={"title": "Asignada a 17", "assignee_id": 17},
    )
    client.post(
        "/tasks",
        json={"title": "Asignada a 18", "assignee_id": 18},
    )

    response = client.get("/tasks", params={"assignee_id": 17})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Asignada a 17"]


def test_list_tasks_combines_status_and_assignee_filters(
    client: TestClient,
) -> None:
    client.post(
        "/tasks",
        json={
            "title": "Coincide",
            "status": "Pendiente",
            "assignee_id": 17,
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Otro responsable",
            "status": "Pendiente",
            "assignee_id": 18,
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Otro estado",
            "status": "En proceso",
            "assignee_id": 17,
        },
    )

    response = client.get(
        "/tasks",
        params={"status": "Pendiente", "assignee_id": 17},
    )

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Coincide"]


def test_list_tasks_without_filters_returns_all_tasks(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Primera"})
    client.post("/tasks", json={"title": "Segunda"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Primera", "Segunda"]


def test_list_tasks_with_no_matches_returns_empty_list(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Pendiente", "status": "Pendiente"})

    response = client.get("/tasks", params={"status": "Terminada"})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "filters",
    [
        {"status": "Desconocido"},
        {"assignee_id": 0},
        {"assignee_id": -1},
    ],
)
def test_list_tasks_rejects_invalid_filters(
    client: TestClient,
    filters: dict[str, str | int],
) -> None:
    response = client.get("/tasks", params=filters)

    assert response.status_code == 422
