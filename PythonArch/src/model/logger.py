from pydantic import BaseModel, Field


class LoggerModel(BaseModel):
    status: str = Field(..., max_length=256)
    type: str = Field(..., max_length=256)
    service: str = Field(..., max_length=256)
    msg: str = Field(..., max_length=2056)
