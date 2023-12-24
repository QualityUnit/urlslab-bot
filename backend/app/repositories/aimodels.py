import json
from redis import Redis
from backend.app.models.aimodel import AIModel

AI_MODEL_KEY_PREFIX = "urlslab_bot_ai_model_"


class SettingsRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get_by_id(self, user_id: int):
        ai_model = self.redis_client.get(f"{AI_MODEL_KEY_PREFIX}{user_id}")
        if ai_model is None:
            return None
        return AIModel(**json.loads(ai_model))

    def upsert(self, user_id: int, ai_model: AIModel):
        self.redis_client.set(f"{AI_MODEL_KEY_PREFIX}{user_id}", json.dumps(ai_model.to_dict()))
