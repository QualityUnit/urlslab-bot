from pydantic import BaseModel, Field


class EmbeddingModelResponse(BaseModel):
    embedding_model_class: str = Field(..., description="AI Model Class", example="OpenAIEmbeddings")
    embedding_model_name: str = Field(..., description="AI Model Name", example="ada2")

    class Config:
        from_attributes = True
