from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


MemberName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=120),
]


class MemberCreate(BaseModel):
    name: MemberName


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
