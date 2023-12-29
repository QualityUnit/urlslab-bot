from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from backend.app.models import Chatbot
from backend.core.repository import BaseRepository


class ChatbotRepository(BaseRepository[Chatbot]):
    """
    Chatbot repository provides all the database operations for the Chatbot model.
    """

    async def get_by_tenant_id(self,
                               tenant_id: int,
                               join_: set[str] | None = None) -> list[Chatbot]:
        """
        Get all chatbots associated to current tenant id.

        :param tenant_id: The tenant id to match.
        :param join_: The joins to make.
        :return: A list of tenants.
        """
        query = self._query(join_)
        query = self._get_by(query, "tenant_id", tenant_id)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._all(query)

    async def get_by_id(self, tenant_id: int, chatbot_id: int) -> Chatbot:
        """
        Get chatbot by id.

        :param tenant_id:  The tenant id to match.
        :param chatbot_id: The chatbot id to match.
        :return: A chatbot.
        """
        query = self._query()
        query = self._get_by(query, "id", chatbot_id)
        query = self._get_by(query, "tenant_id", tenant_id)
        return await self._first(query)

    def _join_tenant(self, query: Select) -> Select:
        """
        Join the author relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Chatbot.tenant))

    async def update(self, attributes: dict[str, Any] = None) -> Chatbot:
        """
        Updates the model instance.

        :param attributes: The attributes to update the model with.
        :return: The updated model instance.
        """
        async with self.session_factory() as session:
            chatbot = await session.get(Chatbot, attributes["id"])
            chatbot.title = attributes["title"]
            chatbot.system_prompt = attributes["system_prompt"]
            chatbot.chat_model_class = attributes["chat_model_class"]
            chatbot.chat_model_name = attributes["chat_model_name"]
            chatbot.tenant_id = attributes["tenant_id"]
            await session.commit()
            return Chatbot(**attributes)

