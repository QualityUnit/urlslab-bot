from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    title: str = Field(..., description="The title of the document", example="document title")
    content: str = Field(..., description="The content of the document", example="document content")
    document_id: str = Field(..., description="Document ID", example="00000000-0000-0000-0000-000000000000")
    source: str = Field(..., description="Document source", example="document source")
    tenant_id: int = Field(..., description="Tenant ID", example=1)
    score: Optional[float] = Field(..., description="Document score", example=0.1)
    updated_at: str = Field(..., description="Document updated at", example="2021-01-01T00:00:00.000000")

    class Config:
        from_attributes = True


class DocumentSource(BaseModel):
    source: str = Field(..., description="Document source", example="document source")
    title: str = Field(..., description="The title of the document", example="document title")

