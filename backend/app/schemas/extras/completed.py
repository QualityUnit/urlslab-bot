from pydantic import BaseModel, Field


class Completed(BaseModel):
    status: str = Field(..., example="OK")
