import uuid
from typing import List, Union
from uuid import UUID

from qdrant_client import AsyncQdrantClient, models

from app.models.document import UrlslabDocument
from core.config import config


class DocumentRepository:
    def __init__(self, qdrant_client: AsyncQdrantClient):
        self.qdrant_client = qdrant_client
        self.collection_name = config.QDRANT_COLLECTION_NAME

    async def get_by_id(self, tenant_id: str, document_id: UUID) -> List[UrlslabDocument]:
        """
        Gets the document by its id
        :return: UrlslabDocument The document to be returned with the given id
        """
        documents = await self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=tenant_id),
                    ),
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=str(document_id)),
                    ),
                ]
            ),
            limit=50,
        )
        return self._convert_qdrant_docs_to_urlslab_docs(documents[0])

    async def get_by_tenant_id(self, tenant_id: str) -> List[UrlslabDocument]:
        """
        Gets all documents by tenant id
        :return: UrlslabDocument The document to be returned related to tenant_id
        """
        documents = await self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=tenant_id),
                    ),
                ]
            ),
            limit=50,
        )
        return self._convert_qdrant_docs_to_urlslab_docs(documents[0])

    async def search_by_tenant_id(self,
                                  tenant_id: str,
                                  query_vector: list[float],
                                  **kwargs) -> List[UrlslabDocument]:
        """
        Gets all documents by tenant id
        :return: UrlslabDocument The document to be returned related to tenant_id
        """
        document_filter = kwargs.get("filter")
        must_filter = [
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value=tenant_id),
            ),
        ]
        if document_filter is not None:
            for f in self.parse_filter(document_filter):
                must_filter.append(f)

        documents = await self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=models.Filter(
                must=must_filter
            ),
            score_threshold=kwargs.get("score_threshold", 0.1),
            limit=10,
        )
        return self._convert_qdrant_docs_to_urlslab_docs(documents)

    async def upsert(self,
                     tenant_id: str,
                     documents: list[UrlslabDocument]) -> list[UrlslabDocument]:
        """
        Upserts the document
        :return: UrlslabDocument The document to be returned with the given id
        """
        await self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    payload={
                        "tenant_id": tenant_id,
                        "document_id": str(doc.document_id),
                        "title": doc.title,
                        "content": doc.content,
                        "source": doc.source,
                        "chunk_id": doc.chunk_id,
                        "updated_at": doc.updated_at,
                        "is_global": tenant_id is None,
                    },
                    vector=doc.vector,
                ) for doc in documents
            ]
        )
        return documents

    async def delete_by_id(self, tenant_id: str, document_ids: list[str]):
        """
        Deletes the document
        :return: None
        """
        await self.qdrant_client.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key='tenant_id',
                        match=models.MatchValue(value=tenant_id)
                    )
                ],
                should=[
                    models.FieldCondition(
                        key='document_id',
                        match=models.MatchValue(value=document_id)
                    ) for document_id in document_ids
                ]
            )
        )

    @staticmethod
    def parse_filter(filter: dict) -> models.Filter:
        """
        Parses the filter
        :return: models.Filter
        """
        must = []
        should = []
        for key, value in filter.items():
            if key == "should":
                for should_filter in value:
                    should.append(
                        models.FieldCondition(
                            key=should_filter["key"],
                            match=models.MatchValue(value=should_filter["value"]),
                        )
                    )
            elif key == "must":
                for must_filter in value:
                    must.append(
                        models.FieldCondition(
                            key=must_filter["key"],
                            match=models.MatchValue(value=must_filter["value"]),
                        )
                    )
            else:
                must.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value),
                    )
                )
        return models.Filter(must=must, should=should)

    @staticmethod
    def _convert_qdrant_docs_to_urlslab_docs(qdrant_docs: Union[List[models.Record], List[models.ScoredPoint]]):
        returning_model = []
        for document in qdrant_docs:
            returning_model.append(
                UrlslabDocument(
                    point_id=document.id,
                    document_id=document.payload["document_id"],
                    title=document.payload["title"],
                    content=document.payload["content"],
                    source=document.payload["source"],
                    tenant_id=document.payload["tenant_id"],
                    chunk_id=document.payload["chunk_id"],
                    updated_at=document.payload["updated_at"],
                    vector=document.vector,
                )
            )
        return returning_model
