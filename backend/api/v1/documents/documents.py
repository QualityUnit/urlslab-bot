from typing import Callable
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from backend.app.controllers import TenantController
from backend.app.controllers.document import DocumentController
from backend.app.models.tenant import TenantPermission
from backend.app.schemas.extras.completed import Completed
from backend.app.schemas.requests.document import DocumentUpsert
from backend.app.schemas.responses.documents import DocumentResponse
from backend.core.factory import Factory
from backend.core.fastapi.dependencies.permissions import Permissions

document_router = APIRouter()


@document_router.get("/{tenant_id}/{document_id}", response_model=DocumentResponse)
async def get_document(
        tenant_id: int,
        document_id: str,
        request: Request,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> DocumentResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await document_controller.get_by_id(request.user.id,
                                               tenant_id,
                                               document_id)


@document_router.get("/{tenant_id}", response_model=list[DocumentResponse])
async def get_documents(
        tenant_id: int,
        request: Request,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> list[DocumentResponse]:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await document_controller.get_by_tenant_id(request.user.id, tenant_id)


@document_router.post("/upsert/{tenant_id}", response_model=DocumentResponse)
async def upsert_document(
        tenant_id: int,
        request: Request,
        document_upsert: DocumentUpsert,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.CREATE)),
) -> DocumentResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await document_controller.upsert_single(request.user.id,
                                                   tenant_id,
                                                   document_upsert)


@document_router.post("/upsert/bulk/{tenant_id}", response_model=list[DocumentResponse])
async def upsert_documents(
        tenant_id: int,
        request: Request,
        document_upsert: list[DocumentUpsert],
        document_controller: DocumentController = Depends(Factory().get_document_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.CREATE)),
) -> list[DocumentResponse]:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await document_controller.upsert_bulk(request.user.id,
                                                 tenant_id,
                                                 document_upsert)


@document_router.delete("/{tenant_id}/{document_id}", response_model=Completed)
async def delete_document(
        tenant_id: int,
        request: Request,
        document_id: str,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> Completed:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    await document_controller.delete_by_id(request.user.id, tenant_id, UUID(document_id))
    return Completed(status="success")
