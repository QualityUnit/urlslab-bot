from typing import Callable
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from backend.app.controllers import TenantController
from backend.app.models import User
from backend.app.models.tenant import TenantPermission

from backend.app.schemas.requests.tenant import TenantCreate
from backend.app.schemas.responses.tenants import TenantResponse
from backend.core.factory import Factory
from backend.core.fastapi.dependencies.current_user import get_current_user
from backend.core.fastapi.dependencies.permissions import Permissions

tenant_router = APIRouter()


@tenant_router.get("/", response_model=list[TenantResponse])
async def get_tenants(
    request: Request,
    tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
    assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> list[TenantResponse]:
    tenants = await tenant_controller.get_by_user_id(request.user.id)

    assert_access(tenants)
    return tenants


@tenant_router.post("/", response_model=TenantResponse, status_code=201)
async def create_tenant(
    request: Request,
    tenant_create: TenantCreate,
    tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
) -> TenantResponse:
    task = await tenant_controller.add(
        title=tenant_create.title,
        description=tenant_create.description,
        user_id=request.user.id,
    )
    return task


@tenant_router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: int,
    tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
    assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> TenantResponse:
    task = await tenant_controller.get_by_id(tenant_id)

    assert_access(task)
    return task
