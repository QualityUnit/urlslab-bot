from uuid import UUID

from pydantic import BaseModel, Field


class SessionResponse(BaseModel):
    session_id: UUID = None
    created_at: str = Field(..., description="Session created at", example="2021-09-24, 12:00:00")
