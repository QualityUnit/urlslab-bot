from typing import Callable

from fastapi import APIRouter, Depends, Request

from backend.app.controllers import ChatbotController, TenantController
from backend.app.models.tenant import TenantPermission
from backend.app.schemas.requests.chatbot import ChatbotCreate
from backend.app.schemas.responses.chatbot import ChatbotResponse
from backend.core.factory import Factory
from backend.core.fastapi.dependencies.permissions import Permissions

chatbot_router = APIRouter()


@chatbot_router.get("/{tenant_id}", response_model=list[ChatbotResponse])
async def get_chatbots(
        tenant_id: int,
        request: Request,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> list[ChatbotResponse]:
    tenant = await tenant_controller.get_by_id(tenant_id)
    chatbots = await chatbot_controller.get_by_tenant_id(tenant_id)

    assert_access(tenant)
    return chatbots


@chatbot_router.post("/{tenant_id}", response_model=ChatbotResponse, status_code=201)
async def create_chatbots(
        tenant_id: int,
        request: Request,
        chatbot_create: ChatbotCreate,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.CREATE)),
) -> ChatbotResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await chatbot_controller.add(
        chatbot_create.title, tenant_id, chatbot_create.system_prompt
    )


@chatbot_router.get("/{tenant_id}/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(
        tenant_id: int,
        chatbot_id: int,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> ChatbotResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)
    return await chatbot_controller.get_by_id(chatbot_id)
