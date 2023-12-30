
from app.models import Tenant
from app.repositories import TenantRepository
from core.controller import BaseController


class TenantController(BaseController[Tenant]):
    """Task controller."""

    def __init__(self, tenant_repository: TenantRepository):
        super().__init__(model=Tenant, repository=tenant_repository)
        self.tenant_repository = tenant_repository

    async def add(self, title: str, description: str) -> Tenant:
        """
        Adds a tenant.

        :param title: The task title.
        :param description: The task description.
        :return: The task.
        """

        return await self.tenant_repository.create(
            {
                "title": title,
                "description": description,
            }
        )
