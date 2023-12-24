import json
from uuid import UUID

from redis import Redis

from backend.app.models import ChatSession
from backend.app.models.aimodel import AIModel

SESSION_KEY_PREFIX = "urlslab_bot_session_"


class SessionRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get_by_id(self, session_id: UUID):
        session = self.redis_client.get(f"{SESSION_KEY_PREFIX}{str(session_id)}")
        if session is None:
            return None
        return ChatSession.from_dict(json.loads(session))

    def add(self, session: ChatSession, ttl=900):
        self.redis_client.set(
            f"{SESSION_KEY_PREFIX}{str(session.session_id)}",
            json.dumps(session.to_dict()),
            ex=ttl
        )
        return session

    def delete(self, session_id: UUID):
        self.redis_client.delete(f"{SESSION_KEY_PREFIX}{str(session_id)}")
