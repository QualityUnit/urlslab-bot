import uuid
from uuid import UUID

from backend.app.models.aimodel import UrlslabEmbeddingModel
from backend.app.models.document import UrlslabDocument, join_document_chunks
from backend.app.repositories.aimodels import SettingsRepository
from backend.app.repositories.document import DocumentRepository
from backend.app.schemas.requests.document import DocumentUpsert
from backend.app.schemas.responses.documents import DocumentResponse
from backend.core.exceptions import BadRequestException, NotFoundException
from backend.core.utils.document_splitter import UrlslabDocumentSplitter


class DocumentController:
    def __init__(self, document_repository: DocumentRepository, settings_repository: SettingsRepository):
        self.document_repository = document_repository
        self.settings_repository = settings_repository

    async def get_by_id(self,
                        user_id: int,
                        tenant_id: int,
                        document_id: str):
        try:
            document_id = UUID(document_id)
        except ValueError:
            raise BadRequestException("Invalid document ID")

        urlslab_docs = await self.document_repository.get_by_id(user_id, tenant_id, document_id)
        if len(urlslab_docs) == 0:
            raise NotFoundException("Document not found")

        return self._convert_docs_to_response(urlslab_docs, merge=True)

    async def get_by_tenant_id(self, user_id: int, tenant_id: int):
        urlslab_docs = await self.document_repository.get_by_tenant_id(user_id, tenant_id)
        return self._convert_docs_to_response(urlslab_docs)

    async def upsert_single(self, user_id: int, tenant_id: int, documents_upsert: DocumentUpsert):
        rsp = await self.upsert(user_id, tenant_id, [documents_upsert])
        return self._convert_docs_to_response(rsp, merge=True)

    async def upsert_bulk(self, user_id: int, tenant_id: int, documents_upsert: list[DocumentUpsert]):
        rsp = await self.upsert(user_id, tenant_id, documents_upsert)
        return self._convert_docs_to_response(rsp)

    async def upsert(self, user_id: int, tenant_id: int, documents_upsert: list[DocumentUpsert]):
        docs = self._convert_document_upsert_to_urlslab_document(tenant_id, documents_upsert)
        doc_ids = set([doc.document_id for doc in docs])
        if doc_ids is not None and len(doc_ids) > 0:
            # document ID provided, check if it exists
            await self.document_repository.delete_by_id(user_id,
                                                        tenant_id,
                                                        list(doc_ids))

        # Add document ID to the documents with no ID
        for doc in docs:
            if doc.document_id is None:
                doc.document_id = uuid.uuid4()

        # start inserting the document
        user_ai_model = self.settings_repository.get_by_id(user_id)
        split_docs = await self._split_and_vectorize_doc(docs, user_ai_model.embedding_model)
        return await self.document_repository.upsert(user_id, tenant_id, split_docs)

    async def delete_by_id(self, user_id: int, tenant_id: int, document_id: UUID):
        await self.document_repository.delete_by_id(user_id, tenant_id, [document_id])

    @staticmethod
    def _convert_document_upsert_to_urlslab_document(tenant_id: int,
                                                     documents_upsert: list[DocumentUpsert]):
        docs = []
        for doc in documents_upsert:
            docs.append(UrlslabDocument(
                document_id=doc.document_id,
                title=doc.document_title,
                content=doc.document_content,
                source=doc.document_source,
                tenant_id=tenant_id,
                chunk_id=None,
                point_id=None,
            ))
        return docs

    @staticmethod
    def _convert_docs_to_response(docs: list[UrlslabDocument], merge=False):
        if len(docs) == 0 or docs is None:
            return []

        # convert to document response
        if merge:
            return DocumentResponse(**join_document_chunks(docs).to_dict())
        else:
            return list(map(lambda doc: DocumentResponse(**doc.to_dict()), docs))

    @staticmethod
    async def _split_and_vectorize_doc(docs: list[UrlslabDocument],
                                       embedding_model: UrlslabEmbeddingModel) -> list[UrlslabDocument]:
        # split the document into chunks
        document_splitter = UrlslabDocumentSplitter(docs)
        indexing_docs = document_splitter.split()
        for indexing_doc in indexing_docs:
            vector = await embedding_model.aembed_query(indexing_doc.content)
            indexing_doc.vector = vector
        return indexing_docs
