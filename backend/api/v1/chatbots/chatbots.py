from fastapi import APIRouter, Depends

from backend.app.controllers import ChatbotController, TenantController
from backend.app.schemas.requests.chatbot import ChatbotCreate
from backend.app.schemas.responses.chatbot import ChatbotResponse
from backend.core.factory import Factory

chatbot_router = APIRouter()


@chatbot_router.get("/{tenant_id}", response_model=list[ChatbotResponse])
async def get_chatbots(
        tenant_id: int,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> list[ChatbotResponse]:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    chatbots = await chatbot_controller.get_by_tenant_id(tenant_id)
    return chatbots


@chatbot_router.post("/{tenant_id}", response_model=ChatbotResponse, status_code=201)
async def create_chatbot(
        tenant_id: int,
        chatbot_create: ChatbotCreate,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    return await chatbot_controller.add(
        chatbot_create.title,
        tenant_id,
        chatbot_create.system_prompt,
        chatbot_create.chat_model_class,
        chatbot_create.chat_model_name,
    )


@chatbot_router.post("/{tenant_id}/{chatbot_id}", response_model=ChatbotResponse, status_code=200)
async def update_chatbot(
        tenant_id: int,
        chatbot_id: int,
        chatbot_create: ChatbotCreate,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    return await chatbot_controller.update(
        chatbot_id,
        chatbot_create.title,
        tenant_id,
        chatbot_create.system_prompt,
        chatbot_create.chat_model_class,
        chatbot_create.chat_model_name,
    )


@chatbot_router.get("/{tenant_id}/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(
        tenant_id: int,
        chatbot_id: int,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    return await chatbot_controller.get_by_id_and_tenant_id(tenant_id, chatbot_id)
