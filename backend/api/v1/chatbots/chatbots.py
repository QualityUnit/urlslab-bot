from fastapi import APIRouter, Depends, Security

from backend.app.controllers import ChatbotController
from backend.app.schemas.requests.chatbot import ChatbotCreate
from backend.app.schemas.responses.chatbot import ChatbotResponse
from backend.core.factory import Factory

chatbot_router = APIRouter()


@chatbot_router.get("/{tenant_id}", response_model=list[ChatbotResponse])
async def get_chatbots(
        tenant_id: int,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> list[ChatbotResponse]:
    chatbots = await chatbot_controller.get_by_tenant_id(tenant_id)
    return chatbots


@chatbot_router.post("/{tenant_id}", response_model=ChatbotResponse, status_code=201)
async def create_chatbots(
        tenant_id: int,
        chatbot_create: ChatbotCreate,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    return await chatbot_controller.add(
        chatbot_create.title, tenant_id, chatbot_create.system_prompt
    )


@chatbot_router.get("/{tenant_id}/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(
        tenant_id: int,
        chatbot_id: int,
        chatbot_controller: ChatbotController = Depends(Factory().get_chatbot_controller),
) -> ChatbotResponse:
    return await chatbot_controller.get_by_id_and_tenant_id(tenant_id, chatbot_id)
