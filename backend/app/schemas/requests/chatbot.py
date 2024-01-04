from typing import Optional

from typing_extensions import Annotated

from pydantic import BaseModel, Field, AfterValidator


BLACKLISTED_PARAMS = ["tenant_id", "document_id", "source", "title"]


def check_blacklisted_params(v):
    for key in v.keys():
        if key in BLACKLISTED_PARAMS:
            raise ValueError(f"Param {key} is not allowed")


ChatbotFilter = Annotated[dict, AfterValidator(check_blacklisted_params)]


class ChatbotCreate(BaseModel):
    title: str = Field(max_length=100, example="Tenant 1")
    system_prompt: str
    chat_model_class: str = Field(..., description="AI Model Class", example="OpenAI")
    chat_model_name: str = Field(..., description="AI Model Name", example="GPT-4")
    chatbot_filter: Optional[ChatbotFilter] = Field(None, description="Chatbot Filter", example={"name": "value"})
