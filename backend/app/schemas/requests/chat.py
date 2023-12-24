from pydantic import BaseModel, Field


class ChatCompletionRequest(BaseModel):
    human_input: str = Field(..., description="Human input", example="Hello, how are you?")
