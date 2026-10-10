from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = None
    status: str = "Pendiente"
    priority: str = "Media"
    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_id: int | None = None

    @field_validator("title", "status", "priority")
    @classmethod
    def reject_null_required_fields(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Este campo no puede ser null.")
        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: str
    priority: str
    assignee_id: int | None
