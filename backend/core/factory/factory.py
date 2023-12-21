from functools import partial

from fastapi import Depends

from backend.app.controllers import AuthController, UserController, TenantController
from backend.app.models import User, Tenant
from backend.app.repositories import UserRepository, TenantRepository
from backend.core.database.session import SessionLocal


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application. Basically, the DI container.
    """

    # Repositories
    user_repository = partial(UserRepository, User)
    tenant_repository = partial(TenantRepository, Tenant)

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
