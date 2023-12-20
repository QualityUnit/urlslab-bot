from backend.app.models import Tenant
from backend.app.repositories import TenantRepository
from backend.core.controller import BaseController
from backend.core.database.transactional import Transactional, Propagation


class TenantController(BaseController[Tenant]):
    """Task controller."""

    def __init__(self, tenant_repository: TenantRepository):
        super().__init__(model=Tenant, repository=tenant_repository)
        self.tenant_repository = tenant_repository

    async def get_by_user_id(self, user_id: int) -> list[Tenant]:
        """
        Returns a list of tenants based on user_id.

        :param user_id: The user id.
        :return: A list of tenants.
        """

        return await self.tenant_repository.get_by_user_id(user_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, title: str, description: str, user_id: int) -> Tenant:
        """
        Adds a task.

        :param title: The task title.
        :param description: The task description.
        :param user_id: The user id.
        :return: The task.
        """

        return await self.tenant_repository.create(
            {
                "title": title,
                "description": description,
                "user_id": user_id,
            }
        )