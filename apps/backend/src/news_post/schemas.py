import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.json_schema import SkipJsonSchema


class CreateNewsPostRequest(BaseModel):
    author: str
    title: str
    content: str


class UpdateNewsPostRequest(BaseModel):
    author: str | SkipJsonSchema[None] = None
    title: str | SkipJsonSchema[None] = None
    content: str | SkipJsonSchema[None] = None

    @field_validator("author", "title", "content")
    @classmethod
    def forbid_null(cls, value: str | None):
        if value is None:
            raise ValueError("Field cannot be null")
        return value


class NewsPostSchema(BaseModel):
    id: uuid.UUID

    author: str
    title: str
    content: str

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
