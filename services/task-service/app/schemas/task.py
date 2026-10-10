from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    title: str = Field(min_length=1, max_length=120)
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: int | None = None

    @field_validator("title", "status", "priority")
    @classmethod
    def reject_null_required_fields(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Este campo no puede ser null.")
        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    assignee_id: int | None
