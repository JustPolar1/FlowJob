from dataclasses import dataclass, replace
from threading import Lock


@dataclass(frozen=True)
class TaskRecord:
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    assignee_id: int | None


class TaskNotFoundError(Exception):
    def __init__(self, task_id: int) -> None:
        super().__init__(f"No existe una tarea con id {task_id}.")


class TaskRepository:
    """Temporary in-memory repository, to be replaced by SQLite in B10."""

    def __init__(self) -> None:
        self._tasks: dict[int, TaskRecord] = {}
        self._next_id = 1
        self._lock = Lock()

    def create(self, values: dict) -> TaskRecord:
        with self._lock:
            task = TaskRecord(id=self._next_id, **values)
            self._tasks[task.id] = task
            self._next_id += 1
            return task

    def list(self) -> list[TaskRecord]:
        with self._lock:
            return list(self._tasks.values())

    def get(self, task_id: int) -> TaskRecord:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise TaskNotFoundError(task_id)
            return task

    def update(self, task_id: int, changes: dict) -> TaskRecord:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise TaskNotFoundError(task_id)
            updated_task = replace(task, **changes)
            self._tasks[task_id] = updated_task
            return updated_task

    def delete(self, task_id: int) -> None:
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(task_id)
            del self._tasks[task_id]
