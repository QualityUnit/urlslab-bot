import json
from redis import Redis
from app.models.aimodel import UrlslabEmbeddingModel
from core.config import config


class SettingsRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.redis_embedding_model_key = config.REDIS_EMBEDDING_MODEL_KEY
        self.version_key = config.VERSION_KEY

    def get_embedding_model(self):
        embedding_model = self.redis_client.get(self.redis_embedding_model_key)
        if embedding_model is None:
            return None
        return UrlslabEmbeddingModel(**json.loads(embedding_model))

    def get_last_version(self):
        last_version = self.redis_client.get(self.version_key)
        if last_version is None:
            return "1.0.0"
        return last_version

    def set_embedding_model(self, embedding_model: UrlslabEmbeddingModel):
        self.redis_client.set(self.redis_embedding_model_key, json.dumps(embedding_model.to_dict()))

    def set_last_version(self, version):
        self.redis_client.set(self.version_key, version)
