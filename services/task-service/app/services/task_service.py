from app.clients import member_client
from app.repositories.task_repository import TaskNotFoundError, TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

repository = TaskRepository()


class AssigneeNotFoundError(Exception):
    """Raised when an assignment references a member that does not exist."""

    def __init__(self, member_id: int) -> None:
        super().__init__(f"No existe un integrante con id {member_id}.")


def _validate_assignee(assignee_id: int | None) -> None:
    """Validate non-null assignee IDs against the Member Service."""
    if assignee_id is not None and not member_client.member_exists(assignee_id):
        raise AssigneeNotFoundError(assignee_id)


def create_task(payload: TaskCreate) -> TaskResponse:
    _validate_assignee(payload.assignee_id)
    record = repository.create(payload.model_dump())
    return TaskResponse.model_validate(record)


def list_tasks() -> list[TaskResponse]:
    return [TaskResponse.model_validate(record) for record in repository.list()]


def get_task(task_id: int) -> TaskResponse:
    return TaskResponse.model_validate(repository.get(task_id))


def update_task(task_id: int, payload: TaskUpdate) -> TaskResponse:
    changes = payload.model_dump(exclude_unset=True)
    if "assignee_id" in changes:
        repository.get(task_id)
        _validate_assignee(changes["assignee_id"])
    record = repository.update(task_id, changes)
    return TaskResponse.model_validate(record)


def delete_task(task_id: int) -> None:
    repository.delete(task_id)
