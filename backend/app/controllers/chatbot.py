import json
from typing import Optional
from uuid import UUID

from app.models import Chatbot
from app.repositories import ChatbotRepository, TenantRepository
from app.schemas.responses.chatbot import ChatbotResponse
from core.controller import BaseController
from core.exceptions import NotFoundException


class ChatbotController(BaseController[Chatbot]):

    def __init__(self, chatbot_repository: ChatbotRepository):
        super().__init__(model=Chatbot, repository=chatbot_repository)
        self.chatbot_repository = chatbot_repository

    async def get_by_tenant_id(self, tenant_id: str) -> list[Chatbot]:
        """
        Returns a list of chatbots based on tenant_id.
        :param tenant_id: the tenant id, the chatbots belong to
        :return: the list of chatbots
        """
        return await self.chatbot_repository.get_by_tenant_id(tenant_id=tenant_id)

    async def get_by_id_and_tenant_id(self, tenant_id: str, chatbot_id: UUID) -> ChatbotResponse:
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
                  tenant_id: str,
                  system_prompt: str,
                  chat_model_class: str,
                  chat_model_name: str,
                  chatbot_filter: dict | None) -> Chatbot:
        """
        Adds a Chatbot
        :param chatbot_filter: filter used to retrieve documents for chatbot
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
                "chatbot_filter": None if chatbot_filter is None else json.dumps(chatbot_filter),
            }
        )

    async def update(self,
                     id: str,
                     title: str,
                     tenant_id: str,
                     system_prompt: str,
                     chat_model_class: str,
                     chat_model_name: str,
                     chatbot_filter: dict) -> Chatbot:
        """
        Adds a Chatbot
        :param chatbot_filter: filter used to retrieve documents for chatbot
        :param id: the id of the chatbot
        :param chat_model_class: the chat model class
        :param chat_model_name: the chat model name
        :param title: the title of the chatbot
        :param tenant_id: the tenant id
        :param system_prompt: the system prompt
        :return: the chatbot object that was created
        """
        chatbot_exists = await self.chatbot_repository.get_by_id(tenant_id=tenant_id, chatbot_id=id)
        if not chatbot_exists:
            raise NotFoundException(f"Chatbot with id {id} and tenant id {tenant_id} not found")

        return await self.chatbot_repository.update(
            {
                "id": id,
                "title": title,
                "system_prompt": system_prompt,
                "tenant_id": tenant_id,
                "chat_model_class": chat_model_class,
                "chat_model_name": chat_model_name,
                "chatbot_filter": None if chatbot_filter is None else json.dumps(chatbot_filter),
            }
        )

    async def delete_chatbot(self, id: str, tenant_id: str) -> None:
        """
        Deletes a Chatbot
        :param id: the id of the chatbot
        :param tenant_id:  the tenant id
        :return:
        """
        chatbot = await self.chatbot_repository.get_by_id(tenant_id=tenant_id, chatbot_id=id)
        if not chatbot:
            raise NotFoundException(f"Chatbot with id {id} and tenant id {tenant_id} not found")

        await self.chatbot_repository.delete(chatbot)
