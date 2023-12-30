from functools import partial

from app.controllers import TenantController, ChatbotController
from app.controllers.aimodels import SettingsController
from app.controllers.document import DocumentController
from app.controllers.session import SessionController
from app.models import Tenant, Chatbot
from app.repositories import TenantRepository, ChatbotRepository
from app.repositories.aimodels import SettingsRepository
from app.repositories.document import DocumentRepository
from app.repositories.session import SessionRepository
from core.database import qdrant_client, redis_client
from core.database.session import SessionLocal


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application. Basically, the DI container.
    """

    # Repositories
    tenant_repository = partial(TenantRepository, Tenant)
    chatbot_repository = partial(ChatbotRepository, Chatbot)
    document_repository = partial(DocumentRepository)
    settings_repository = partial(SettingsRepository)
    session_repository = partial(SessionRepository)

    def get_tenant_controller(self):
        return TenantController(
            tenant_repository=self.tenant_repository(session_factory=SessionLocal)
        )

    def get_chatbot_controller(self):
        return ChatbotController(
            chatbot_repository=self.chatbot_repository(session_factory=SessionLocal)
        )

    def get_document_controller(self):
        return DocumentController(document_repository=self.document_repository(qdrant_client=qdrant_client),
                                  settings_repository=self.settings_repository(redis_client=redis_client))

    def get_ai_model_controller(self):
        return SettingsController(settings_repository=self.settings_repository(redis_client=redis_client))

    def get_session_controller(self):
        return SessionController(session_repository=self.session_repository(redis_client=redis_client),
                                 document_repository=self.document_repository(qdrant_client=qdrant_client),
                                 tenant_repository=self.tenant_repository(session_factory=SessionLocal),
                                 chatbot_repository=self.chatbot_repository(session_factory=SessionLocal),
                                 settings_repository=self.settings_repository(redis_client=redis_client))
