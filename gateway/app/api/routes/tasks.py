from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.core.config import settings
from app.core.proxy import forward_request


router = APIRouter(prefix="/tasks")
TASK_METHODS = ["GET", "POST", "PATCH", "DELETE"]


@router.api_route("", methods=TASK_METHODS, summary="Forward task collection requests")
async def task_collection(request: Request) -> Response:
    return await forward_request(
        request,
        service_name="task-service",
        service_url=settings.task_service_url,
        service_path="tasks",
    )


@router.api_route(
    "/{path:path}",
    methods=TASK_METHODS,
    summary="Forward task resource requests",
)
async def task_resource(path: str, request: Request) -> Response:
    return await forward_request(
        request,
        service_name="task-service",
        service_url=settings.task_service_url,
        service_path=f"tasks/{path}",
    )
