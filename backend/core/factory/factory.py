from functools import partial

from fastapi import Depends

from backend.app.controllers import AuthController, UserController, TenantController, ChatbotController
from backend.app.models import User, Tenant, Chatbot
from backend.app.repositories import UserRepository, TenantRepository, ChatbotRepository
from backend.core.database.session import SessionLocal


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application. Basically, the DI container.
    """

    # Repositories
    user_repository = partial(UserRepository, User)
    tenant_repository = partial(TenantRepository, Tenant)
    chatbot_repository = partial(ChatbotRepository, Chatbot)

    def get_user_controller(self):
        return UserController(
            user_repository=self.user_repository(session_factory=SessionLocal)
        )

    def get_auth_controller(self):
        return AuthController(
            user_repository=self.user_repository(session_factory=SessionLocal),
        )

    def get_tenant_controller(self):
        return TenantController(
            tenant_repository=self.tenant_repository(session_factory=SessionLocal)
        )

    def get_chatbot_controller(self):
        return ChatbotController(
            chatbot_repository=self.chatbot_repository(session_factory=SessionLocal),
            tenant_repository=self.tenant_repository(session_factory=SessionLocal)
        )
