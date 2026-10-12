import os

import httpx
from fastapi import APIRouter, HTTPException, Query
from starlette import status


router = APIRouter()
TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://127.0.0.1:8001").rstrip("/")


@router.get("/tasks")
async def list_tasks(
    task_status: str | None = Query(default=None, alias="status"),
    assignee_id: int | None = Query(default=None, ge=1),
) -> list[dict]:
    """Forward task-list requests to the service that owns task data."""
    params = {
        key: value
        for key, value in {"status": task_status, "assignee_id": assignee_id}.items()
        if value is not None
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{TASK_SERVICE_URL}/tasks", params=params)
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de tareas no está disponible.",
        ) from error

    if response.is_error:
        try:
            detail = response.json().get("detail", "No se pudieron consultar las tareas.")
        except ValueError:
            detail = "No se pudieron consultar las tareas."
        raise HTTPException(status_code=response.status_code, detail=detail)

    return response.json()
