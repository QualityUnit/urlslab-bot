from pydantic import BaseModel, Field


class AIModelResponse(BaseModel):
    embedding_model_class: str = Field(..., description="AI Model Class", example="OpenAIEmbeddings")
    embedding_model_name: str = Field(..., description="AI Model Name", example="ada2")
    chat_model_class: str = Field(..., description="AI Model Class", example="OpenAI")
    chat_model_name: str = Field(..., description="AI Model Name", example="GPT-4")

    class Config:
        from_attributes = True
