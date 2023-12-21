from backend.app.models import Chatbot
from backend.app.repositories import ChatbotRepository, TenantRepository
from backend.core.controller import BaseController


class ChatbotController(BaseController[Chatbot]):

    def __init__(self, chatbot_repository: ChatbotRepository, tenant_repository: TenantRepository):
        super().__init__(model=Chatbot, repository=chatbot_repository)
        self.chatbot_repository = chatbot_repository
        self.tenant_repository = tenant_repository

    async def get_by_tenant_id(self, tenant_id: int) -> list[Chatbot]:
        """
        Returns a list of chatbots based on tenant_id.
        :param tenant_id: the tenant id, the chatbots belong to
        :return: the list of chatbots
        """
        return await self.chatbot_repository.get_by_tenant_id(tenant_id=tenant_id)

    async def add(self, title: str, tenant_id: int, system_prompt: str) -> Chatbot:
        """
        Adds a Chatbot
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
            }
        )
