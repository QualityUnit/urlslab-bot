from qdrant_client import AsyncQdrantClient
from core.config import config

qdrant_client: AsyncQdrantClient = AsyncQdrantClient(config.QDRANT_URL)
