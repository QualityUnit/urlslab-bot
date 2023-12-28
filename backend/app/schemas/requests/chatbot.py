from typing_extensions import Annotated

from pydantic import BaseModel, Field


class ChatbotCreate(BaseModel):
    title: str = Field(max_length=100, example="Tenant 1")
    system_prompt: str
    chat_model_class: str = Field(..., description="AI Model Class", example="OpenAI")
    chat_model_name: str = Field(..., description="AI Model Name", example="GPT-4")
