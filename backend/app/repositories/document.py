from qdrant_client import AsyncQdrantClient


class DocumentRepository:
    def __init__(self, qdrant_client: AsyncQdrantClient):
        self.qdrant_client = qdrant_client


