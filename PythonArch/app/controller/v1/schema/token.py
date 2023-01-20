from pydantic import Field

from app.core.schema import BaseSchema

__all__ = ["TokenCreateSchema"]


class TokenCreateSchema(BaseSchema):
    token: str = Field(..., max_length=64)
