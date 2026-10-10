from app.repositories.task_repository import TaskNotFoundError, TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

repository = TaskRepository()


def create_task(payload: TaskCreate) -> TaskResponse:
    record = repository.create(payload.model_dump())
    return TaskResponse.model_validate(record)


def list_tasks() -> list[TaskResponse]:
    return [TaskResponse.model_validate(record) for record in repository.list()]


def get_task(task_id: int) -> TaskResponse:
    return TaskResponse.model_validate(repository.get(task_id))


def update_task(task_id: int, payload: TaskUpdate) -> TaskResponse:
    changes = payload.model_dump(exclude_unset=True)
    record = repository.update(task_id, changes)
    return TaskResponse.model_validate(record)


def delete_task(task_id: int) -> None:
    repository.delete(task_id)
