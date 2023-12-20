from pydantic import UUID4, BaseModel, Field


class TenantResponse(BaseModel):
    title: str = Field(..., description="Tenant name", example="Tenant 1")
    description: str = Field(
        ..., description="Tenant description", example="Tenant 1 description"
    )
    uuid: UUID4 = Field(
        ..., description="Tenant UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )

    class Config:
        from_attributes = True
