import uuid
from typing import List, Union
from uuid import UUID

from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import Payload, Record

from backend.app.models.aimodel import AIModel
from backend.app.models.document import UrlslabDocument

COLLECTION_NAME_PREFIX = "urlslab_bot_user_"


def _collection_name(user_id: int) -> str:
    return f"{COLLECTION_NAME_PREFIX}{user_id}"


class DocumentRepository:
    def __init__(self, qdrant_client: AsyncQdrantClient):
        self.qdrant_client = qdrant_client

    async def get_by_id(self, user_id: int, tenant_id: int, document_id: UUID) -> List[UrlslabDocument]:
        """
        Gets the document by its id
        :return: UrlslabDocument The document to be returned with the given id
        """
        documents = await self.qdrant_client.scroll(
            collection_name=_collection_name(user_id),
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

    async def get_by_tenant_id(self, user_id: int, tenant_id: int) -> List[UrlslabDocument]:
        """
        Gets all documents by tenant id
        :return: UrlslabDocument The document to be returned related to tenant_id
        """
        documents = await self.qdrant_client.scroll(
            collection_name=_collection_name(user_id),
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
                                  user_id: int,
                                  tenant_id: int,
                                  query_vector: list[float],
                                  **kwargs) -> List[UrlslabDocument]:
        """
        Gets all documents by tenant id
        :return: UrlslabDocument The document to be returned related to tenant_id
        """
        documents = await self.qdrant_client.search(
            collection_name=_collection_name(user_id),
            query_vector=query_vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=tenant_id),
                    ),
                ]
            ),
            score_threshold=kwargs.get("score_threshold", 0.5),
            limit=10,
        )
        return self._convert_qdrant_docs_to_urlslab_docs(documents)

    async def upsert(self,
                     user_id: int,
                     tenant_id: int,
                     documents: list[UrlslabDocument]) -> list[UrlslabDocument]:
        """
        Upserts the document
        :return: UrlslabDocument The document to be returned with the given id
        """
        await self.qdrant_client.upsert(
            collection_name=_collection_name(user_id),
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
                    },
                    vector=doc.vector,
                ) for doc in documents
            ]
        )
        return documents

    async def delete_by_id(self, user_id: int, tenant_id: int, document_ids: list[str]):
        """
        Deletes the document
        :return: None
        """
        await self.qdrant_client.delete(
            collection_name=_collection_name(user_id),
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

    async def create_document_index(self,
                                    user_id: int,
                                    user_ai_model: AIModel):
        dim = user_ai_model.embedding_model.embedding_dimensions()
        collection_name = _collection_name(user_id)
        await self.qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=dim,
                distance=models.Distance.COSINE,
                on_disk=True,
            ),
            hnsw_config=models.HnswConfigDiff(
                payload_m=16,
                m=0,
            ),
            shard_number=3,
            replication_factor=2
        )

        # creating index on tenant_id
        await self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="tenant_id",
            field_schema=models.PayloadSchemaType.INTEGER,
        )

        # creating index on document_id
        await self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="document_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

        # creating index for resource source
        await self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="source",
            field_schema=models.PayloadSchemaType.TEXT,
        )

        # creating index for resource title
        await self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="title",
            field_schema=models.PayloadSchemaType.TEXT,
        )

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
