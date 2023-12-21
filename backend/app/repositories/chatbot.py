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

    def _join_tenant(self, query: Select) -> Select:
        """
        Join the author relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Chatbot.tenant))
