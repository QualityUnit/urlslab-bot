import datetime
import typing
import uuid
from uuid import UUID

from fastapi.openapi.models import Response
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tracers import ConsoleCallbackHandler
from starlette.responses import StreamingResponse

from backend.app.models import ChatSession
from backend.app.repositories import TenantRepository, ChatbotRepository
from backend.app.repositories.aimodels import SettingsRepository
from backend.app.repositories.document import DocumentRepository
from backend.app.repositories.session import SessionRepository
from backend.app.schemas.requests.chat import ChatCompletionRequest
from backend.app.schemas.responses.documents import DocumentResponse
from backend.app.schemas.responses.session import SessionResponse
from backend.core.chains import DefaultChainFactory
from backend.core.exceptions import NotFoundException


def _get_default_config():
    return {
        'callbacks': [ConsoleCallbackHandler()],
    }


class SessionController:
    def __init__(self,
                 session_repository: SessionRepository,
                 document_repository: DocumentRepository,
                 tenant_repository: TenantRepository,
                 chatbot_repository: ChatbotRepository,
                 settings_repository: SettingsRepository):
        self.session_repository = session_repository
        self.document_repository = document_repository
        self.tenant_repository = tenant_repository
        self.chatbot_repository = chatbot_repository
        self.settings_repository = settings_repository

    def stream_chatbot_response(self,
                                user_id: int,
                                session_id: UUID,
                                chat_completion_request: ChatCompletionRequest) -> StreamingResponse:
        session = self.session_repository.get_by_id(session_id=session_id)
        if session is None:
            raise NotFoundException("Session not found")

        if session.user_id != user_id:
            raise NotFoundException("Session not found")

        return StreamingResponse(
            self._stream_chatbot_response(user_id, session, chat_completion_request),
            media_type="text/event-stream")

    async def _stream_chatbot_response(self,
                                       user_id: int,
                                       session: ChatSession,
                                       chat_completion_request: ChatCompletionRequest) -> typing.AsyncIterable[str]:
        # creating chain
        chain = DefaultChainFactory(document_repository=self.document_repository,
                                    session=session,
                                    user_id=user_id).create_chain()

        # chain created - updating session message history
        # update history and update ttl
        session.message_history.append(HumanMessage(content=chat_completion_request.human_input))
        self.session_repository.add(session=session)

        ai_response = ""
        async for chunk in chain.astream(
                {"human_input": chat_completion_request.human_input},
                config=_get_default_config()
        ):
            ai_response += chunk
            yield chunk

        # chain finished - updating session message history
        # update history and update ttl
        session.message_history.append(AIMessage(content=ai_response))
        self.session_repository.add(session=session)

        # saving sources used
        self.session_repository.set_session_sources(session_id=session.session_id,
                                                    sources=chain.sources)

    def get_session_last_source(self, user_id: int, session_id: UUID):
        session = self.session_repository.get_by_id(session_id=session_id)
        if session is None:
            raise NotFoundException("Session not found")

        if session.user_id != user_id:
            raise NotFoundException("Session not found")

        sources = self.session_repository.get_session_sources(session_id=session.session_id)
        if sources is None:
            return []

        return [DocumentResponse(**source) for source in sources]

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
