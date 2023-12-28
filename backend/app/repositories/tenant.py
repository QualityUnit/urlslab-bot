from backend.app.models import Tenant
from backend.core.repository import BaseRepository


class TenantRepository(BaseRepository[Tenant]):
    """
    Tenant repository provides all the database operations for the Tenant model.
    """

    async def get_by_id(self, tenant_id: int) -> Tenant:
        """
        Get tenant by id.

        :param tenant_id: The tenant id to match.
        :return: A tenant.
        """
        query = self._query()
        query = self._get_by(query, "id", tenant_id)
        return await self._first(query)
