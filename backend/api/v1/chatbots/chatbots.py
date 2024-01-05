from uuid import UUID

from fastapi import APIRouter, Depends

from app.controllers import ChatbotController, TenantController
from app.schemas.extras.completed import Completed
from app.schemas.requests.chatbot import ChatbotCreate
from app.schemas.responses.chatbot import ChatbotResponse
from core.factory import Factory

chatbot_router = APIRouter()


@chatbot_router.get("/{tenant_id}", response_model=list[ChatbotResponse])
async def get_chatbots(
        tenant_id: str,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> list[ChatbotResponse]:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    chatbots = await chatbot_controller.get_by_tenant_id(tenant_id)
    return chatbots


@chatbot_router.post("/{tenant_id}", response_model=ChatbotResponse, status_code=201)
async def create_chatbot(
        tenant_id: str,
        chatbot_create: ChatbotCreate,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    return await chatbot_controller.add(
        chatbot_create.title,
        tenant_id,
        chatbot_create.system_prompt,
        chatbot_create.chat_model_class,
        chatbot_create.chat_model_name,
        chatbot_create.chatbot_filter,
    )


@chatbot_router.post("/{tenant_id}/{chatbot_id}", response_model=ChatbotResponse, status_code=200)
async def update_chatbot(
        tenant_id: str,
        chatbot_id: str,
        chatbot_create: ChatbotCreate,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    try:
        chatbot_id = UUID(chatbot_id)
    except ValueError:
        raise ValueError(f"Invalid chatbot id {chatbot_id}")

    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    return await chatbot_controller.update(
        chatbot_id,
        chatbot_create.title,
        tenant_id,
        chatbot_create.system_prompt,
        chatbot_create.chat_model_class,
        chatbot_create.chat_model_name,
        chatbot_create.chatbot_filter,
    )


@chatbot_router.delete("/{tenant_id}/{chatbot_id}")
async def delete_chatbot(
        tenant_id: str,
        chatbot_id: str,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> Completed:
    try:
        chatbot_id = UUID(chatbot_id)
    except ValueError:
        raise ValueError(f"Invalid chatbot id {chatbot_id}")

    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    await chatbot_controller.delete_chatbot(
        chatbot_id,
        tenant_id,
    )
    return Completed(status="success")


@chatbot_router.get("/{tenant_id}/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(
        tenant_id: str,
        chatbot_id: str,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    try:
        chatbot_id = UUID(chatbot_id)
    except ValueError:
        raise ValueError(f"Invalid chatbot id {chatbot_id}")

    return await chatbot_controller.get_by_id_and_tenant_id(tenant_id, chatbot_id)
