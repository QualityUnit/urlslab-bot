from pydantic import UUID4, BaseModel, Field


class TenantResponse(BaseModel):
    title: str = Field(..., description="Tenant name", example="Tenant 1")
    description: str = Field(
        ..., description="Tenant description", example="Tenant 1 description"
    )
    id: int = Field(..., description="Tenant id", example=1)

    class Config:
        from_attributes = True
