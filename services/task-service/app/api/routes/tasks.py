from fastapi import APIRouter, HTTPException, Response, status

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    TaskNotFoundError,
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)

router = APIRouter(prefix="/tasks")


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(payload: TaskCreate) -> TaskResponse:
    return create_task(payload)


@router.get("", response_model=list[TaskResponse])
def list_tasks_endpoint() -> list[TaskResponse]:
    return list_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int) -> TaskResponse:
    try:
        return get_task(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, payload: TaskUpdate) -> TaskResponse:
    try:
        return update_task(task_id, payload)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int) -> Response:
    try:
        delete_task(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
