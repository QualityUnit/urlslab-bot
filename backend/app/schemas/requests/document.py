from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentUpsert(BaseModel):
    document_title: str = Field(max_length=100, example="Tenant 1"),
    document_content: str = Field(example="lorem ipsum dolor sit amet"),
    document_id: Optional[UUID] = None
    document_source: Optional[str] = None
