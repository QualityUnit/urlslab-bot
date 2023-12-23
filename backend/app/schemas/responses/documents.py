from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    title: str = Field(..., description="The title of the document", example="document title")
    content: str = Field(..., description="The content of the document", example="document content")
    document_id: UUID = Field(..., description="Document ID", example="00000000-0000-0000-0000-000000000000")
    source: str = Field(..., description="Document source", example="document source")
    tenant_id: int = Field(..., description="Tenant ID", example=1)
    vector: List[float] = Field(..., description="Document vector", example=[0.1, 0.2, 0.3])
    score: float = Field(..., description="Document score", example=0.1)
    created_at: str = Field(..., description="Document created at", example="2021-01-01T00:00:00.000000")
    updated_at: str = Field(..., description="Document updated at", example="2021-01-01T00:00:00.000000")

    class Config:
        from_attributes = True

