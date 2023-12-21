from pydantic import UUID4, BaseModel, Field


class ChatbotResponse(BaseModel):
    title: str = Field(..., description="Tenant name", example="Tenant 1")
    system_prompt: str = Field(
        ..., description="The System Prompt to be used for chatbot", example="You are a helpful assistant."
    )
    id: int = Field(..., description="Chatbot id", example=1)

    class Config:
        from_attributes = True
