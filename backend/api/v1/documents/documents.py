from typing import Callable

from fastapi import APIRouter, Depends, Request

from backend.app.controllers import ChatbotController, TenantController
from backend.app.controllers.document import DocumentController
from backend.app.models.tenant import TenantPermission
from backend.app.schemas.requests.chatbot import ChatbotCreate
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
) -> list[DocumentResponse]:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await document_controller.get_by_id(tenant_id, document_id)


@document_router.get("/{tenant_id}", response_model=list[DocumentResponse])
async def get_documents(
        tenant_id: int,
        document_id: str,
        request: Request,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> list[DocumentResponse]:
    tenant = await tenant_controller.get_by_id(tenant_id)
    chatbots = await chatbot_controller.get_by_tenant_id(tenant_id)

    assert_access(tenant)
    return chatbots


@document_router.post("/upsert/{tenant_id}", response_model=DocumentResponse)
async def upsert_document(
        tenant_id: int,
        request: Request,
        chatbot_create: ChatbotCreate,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.CREATE)),
) -> DocumentResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await chatbot_controller.add(
        chatbot_create.title, tenant_id, chatbot_create.system_prompt
    )


@document_router.post("/upsert/bulk/{tenant_id}", response_model=list[DocumentResponse])
async def upsert_documents(
        tenant_id: int,
        request: Request,
        chatbot_create: ChatbotCreate,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.CREATE)),
) -> DocumentResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await chatbot_controller.add(
        chatbot_create.title, tenant_id, chatbot_create.system_prompt
    )


@document_router.delete("/{tenant_id}/{document_id}", response_model=DocumentResponse)
async def delete_document(
        tenant_id: int,
        document_id: str,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> DocumentResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)
    return await chatbot_controller.get_by_id(chatbot_id)
