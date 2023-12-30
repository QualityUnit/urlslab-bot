import semver
from qdrant_client import QdrantClient, models

from app.repositories.aimodels import SettingsRepository
from core.database import redis_client
from app.models.aimodel import UrlslabEmbeddingModel
from core.config import config


class VersionManager:
    def __init__(self):
        self.qdrant_client: QdrantClient = QdrantClient(config.QDRANT_URL)
        self.redis_client = redis_client
        self.settings_repo = SettingsRepository(redis_client=redis_client)
        self.collection_name = config.QDRANT_COLLECTION_NAME
        self.release_version = config.RELEASE_VERSION

    def setup(self):
        settings_repo = SettingsRepository(redis_client=redis_client)
        embedding_model = settings_repo.get_embedding_model()
        if embedding_model is None:
            # initializing vector database
            embedding_model = UrlslabEmbeddingModel(
                embedding_model_name=config.DEFAULT_EMBEDDING_MODEL_NAME,
                embedding_model_class=config.DEFAULT_EMBEDDING_MODEL_CLASS,
            )
            self.init(embedding_model=embedding_model)
            settings_repo.set_embedding_model(embedding_model=embedding_model)
            settings_repo.set_last_version(version=self.release_version)
        else:
            # update step
            last_version = settings_repo.get_last_version()
            semver_cmp = semver.compare(last_version, self.release_version)
            if semver_cmp == 0:
                # version already up-to-date nothing to do
                pass
            elif semver_cmp < 0:
                # need to update
                self.update(embedding_model=embedding_model, last_version=last_version)
                settings_repo.set_last_version(self.release_version)
            else:
                raise ValueError("Current version bigger than release version. this cannot happen...:)")

        # closing qdrant client. its synchronous client. async client is used in the application.
        self.qdrant_client.close()

    def init(self, embedding_model: UrlslabEmbeddingModel):
        dim = embedding_model.embedding_dimensions()
        collection_name = self.collection_name
        self.qdrant_client.create_collection(
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
        self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="tenant_id",
            field_schema=models.PayloadSchemaType.INTEGER,
        )

        # creating index on document_id
        self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="document_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

        # creating index for resource source
        self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="source",
            field_schema=models.PayloadSchemaType.TEXT,
        )

        # creating index for resource title
        self.qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="title",
            field_schema=models.PayloadSchemaType.TEXT,
        )

    def update(self, embedding_model: UrlslabEmbeddingModel, last_version: str):
        pass
