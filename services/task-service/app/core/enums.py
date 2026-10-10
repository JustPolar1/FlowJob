from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "Pendiente"
    IN_PROGRESS = "En proceso"
    COMPLETED = "Terminada"


class TaskPriority(str, Enum):
    LOW = "Baja"
    MEDIUM = "Media"
    HIGH = "Alta"
