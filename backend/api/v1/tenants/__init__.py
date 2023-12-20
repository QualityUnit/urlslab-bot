from fastapi import APIRouter, Depends

from backend.core.fastapi.dependencies.authentication import AuthenticationRequired

from .tenants import tenant_router

tenants_router = APIRouter()
tenants_router.include_router(
    tenant_router,
    tags=["Tenants"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["tenants_router"]
