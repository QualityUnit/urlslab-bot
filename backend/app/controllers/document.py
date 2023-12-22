from uuid import UUID

from backend.app.repositories.document import DocumentRepository
from backend.core.controller import BaseController


class DocumentController:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    async def get_by_id(self, tenant_id: int, document_id: UUID):
        return await self.document_repository.get_by_id(tenant_id, document_id)


