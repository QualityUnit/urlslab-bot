from backend.app.models import Tenant
from backend.core.repository import BaseRepository


class TenantRepository(BaseRepository[Tenant]):
    """
    Tenant repository provides all the database operations for the Tenant model.
    """

    async def get_by_user_id(self,
                             user_id,
                             join_: set[str] | None = None
                             ) -> list[Tenant]:
        """
        Get all tenants by user id.

        :param user_id: The user id to match.
        :param join_: The joins to make.
        :return: A list of tenants.
        """
        query = self._query(join_)
        query = self._get_by(query, "user_id", user_id)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._all(query)

    async def get_by_id(self, tenant_id: int) -> Tenant:
        """
        Get tenant by id.

        :param tenant_id: The tenant id to match.
        :return: A tenant.
        """
        query = self._query()
        query = self._get_by(query, "id", tenant_id)
        return await self._first(query)
