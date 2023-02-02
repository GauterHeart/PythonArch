from pydantic import BaseModel, Field

from src.core.schema import BaseSchema


class LoggerCreateSchema(BaseModel):
    status: str = Field(..., max_length=256)
    type: str = Field(..., max_length=256)
    service: str = Field(..., max_length=256)
    msg: str = Field(..., max_length=2056)


class LoggerCreateRabbitSchema(LoggerCreateSchema):
    ...


class LoggerCreateHttpSchema(BaseSchema, LoggerCreateSchema):
    ...
