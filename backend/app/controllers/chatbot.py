from backend.app.models import Chatbot
from backend.app.repositories import ChatbotRepository, TenantRepository
from backend.app.schemas.responses.chatbot import ChatbotResponse
from backend.core.controller import BaseController
from backend.core.exceptions import NotFoundException


class ChatbotController(BaseController[Chatbot]):

    def __init__(self, chatbot_repository: ChatbotRepository):
        super().__init__(model=Chatbot, repository=chatbot_repository)
        self.chatbot_repository = chatbot_repository

    async def get_by_tenant_id(self, tenant_id: int) -> list[Chatbot]:
        """
        Returns a list of chatbots based on tenant_id.
        :param tenant_id: the tenant id, the chatbots belong to
        :return: the list of chatbots
        """
        return await self.chatbot_repository.get_by_tenant_id(tenant_id=tenant_id)

    async def get_by_id_and_tenant_id(self, tenant_id: int, chatbot_id: int) -> ChatbotResponse:
        """
        Returns a chatbot based on tenant_id and chatbot_id.
        :param tenant_id: the tenant id, the chatbot belongs to
        :param chatbot_id: the chatbot id
        :return: the chatbot
        """
        chatbot = await self.chatbot_repository.get_by_id(tenant_id=tenant_id, chatbot_id=chatbot_id)
        if not chatbot:
            raise NotFoundException(f"Chatbot with id {chatbot_id} and tenant id {tenant_id} not found")
        return ChatbotResponse(**chatbot.__dict__)

    async def add(self,
                  title: str,
                  tenant_id: int,
                  system_prompt: str,
                  chat_model_class: str,
                  chat_model_name: str) -> Chatbot:
        """
        Adds a Chatbot
        :param chat_model_class: the chat model class
        :param chat_model_name: the chat model name
        :param title: the title of the chatbot
        :param tenant_id: the tenant id
        :param system_prompt: the system prompt
        :return: the chatbot object that was created
        """

        return await self.chatbot_repository.create(
            {
                "title": title,
                "system_prompt": system_prompt,
                "tenant_id": tenant_id,
                "chat_model_class": chat_model_class,
                "chat_model_name": chat_model_name,
            }
        )
