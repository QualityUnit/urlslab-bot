from functools import partial

from fastapi import Depends

from backend.app.controllers import AuthController, UserController, TenantController
from backend.app.models import User, Tenant
from backend.app.repositories import UserRepository, TenantRepository
from backend.core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application. Basically, the DI container.
    """

    # Repositories
    user_repository = partial(UserRepository, User)
    tenant_repository = partial(TenantRepository, Tenant)

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(
            user_repository=self.user_repository(db_session=db_session)
        )

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(
            user_repository=self.user_repository(db_session=db_session),
        )

    def get_tenant_controller(self, db_session=Depends(get_session)):
        return TenantController(
            tenant_repository=self.tenant_repository(db_session=db_session)
        )
