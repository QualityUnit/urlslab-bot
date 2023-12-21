from typing_extensions import Annotated

from pydantic import BaseModel, Field


class ChatbotCreate(BaseModel):
    title: str = Field(max_length=100, example="Tenant 1")
    system_prompt: str
