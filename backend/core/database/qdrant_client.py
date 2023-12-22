from qdrant_client import AsyncQdrantClient
from backend.core.config import config

client: AsyncQdrantClient = AsyncQdrantClient(config.QDRANT_URL)
