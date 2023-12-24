import datetime
import typing
import uuid
from uuid import UUID

from langchain_core.messages import SystemMessage, HumanMessage

from backend.app.models import ChatSession
from backend.app.repositories import TenantRepository, ChatbotRepository
from backend.app.repositories.aimodels import SettingsRepository
from backend.app.repositories.session import SessionRepository
from backend.app.schemas.requests.chat import ChatCompletionRequest
from backend.app.schemas.responses.session import SessionResponse
from backend.core.chains import DefaultChainFactory
from backend.core.exceptions import NotFoundException


class SessionController:
    def __init__(self,
                 session_repository: SessionRepository,
                 tenant_repository: TenantRepository,
                 chatbot_repository: ChatbotRepository,
                 settings_repository: SettingsRepository):
        self.session_repository = session_repository
        self.tenant_repository = tenant_repository
        self.chatbot_repository = chatbot_repository
        self.settings_repository = settings_repository

    def stream_chatbot_response(self,
                                user_id: int,
                                session_id: UUID,
                                chat_completion_request: ChatCompletionRequest) -> typing.AsyncIterable[str]:
        session = self.session_repository.get_by_id(session_id=session_id)
        if session is None:
            raise NotFoundException("Session not found")

        if session.user_id != user_id:
            raise NotFoundException("Session not found")

        # update history and update ttl
        session.message_history.append(HumanMessage(content=chat_completion_request.human_input))
        self.session_repository.add(session=session)

        # creating chain
        chain = DefaultChainFactory(session=session).create_chain()

        for chunk in chain.stream({"human_input": chat_completion_request.human_input}):
            yield chunk

    async def create_session(self,
                             user_id: int,
                             tenant_id: int,
                             chatbot_id: int) -> SessionResponse:
        # retrieving tenant
        tenant = await self.tenant_repository.get_by_id(tenant_id=tenant_id)
        if tenant is None:
            raise NotFoundException("Tenant not found")

        # retrieving chatbot
        chatbot = await self.chatbot_repository.get_by_id(chatbot_id=chatbot_id)
        if chatbot is None:
            raise NotFoundException("Chatbot not found")

        if chatbot.tenant_id != tenant.id:
            raise NotFoundException("Chatbot not found in this tenant")

        # retrieving ai model settings
        ai_model_settings = self.settings_repository.get_by_id(user_id)
        if ai_model_settings is None:
            raise NotFoundException("AI Model settings not found")

        # creating session
        session = self.session_repository.add(
            ChatSession(
                session_id=uuid.uuid4(),
                user_id=user_id,
                tenant_id=tenant_id,
                chatbot_id=chatbot_id,
                ai_model_settings=ai_model_settings,
                message_history=[SystemMessage(content=chatbot.system_prompt)],
                created_at=datetime.datetime.now()
            )
        )

        return SessionResponse(session_id=session.session_id,
                               created_at=session.get_created_at_string())

    def delete_session(self, user_id: int, session_id: UUID):
        session = self.session_repository.get_by_id(session_id=session_id)
        if session is not None:
            if session.user_id == user_id:
                self.session_repository.delete(session_id=session_id)
            else:
                raise NotFoundException("Session not found")
