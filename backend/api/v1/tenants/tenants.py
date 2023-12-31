from fastapi import APIRouter, Depends, Request, Security

from app.controllers import TenantController

from app.schemas.requests.tenant import TenantCreate
from app.schemas.responses.tenants import TenantResponse
from core.factory import Factory

tenant_router = APIRouter()


@tenant_router.get("/", response_model=list[TenantResponse])
async def get_tenants(
    request: Request,
    tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
) -> list[TenantResponse]:
    tenants = await tenant_controller.get_all(request.user.id)
    return tenants


@tenant_router.post("/", response_model=TenantResponse, status_code=201)
async def create_tenant(
    request: Request,
    tenant_create: TenantCreate,
    tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
) -> TenantResponse:
    task = await tenant_controller.add(
        tenant_id=tenant_create.id,
        title=tenant_create.title,
        description=tenant_create.description,
    )
    return task


@tenant_router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
) -> TenantResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    return tenant
