import json
from uuid import UUID

from redis import Redis

from backend.app.models import ChatSession

SESSION_KEY_PREFIX = "urlslab_bot_session_"
SESSION_SOURCES_KEY_PREFIX = "urlslab_bot_session_sources_"


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

    def get_session_sources(self, session_id: UUID):
        sources = self.redis_client.get(f"{SESSION_SOURCES_KEY_PREFIX}{str(session_id)}")
        if sources is None:
            return None
        return json.loads(sources)

    def set_session_sources(self, session_id: UUID, sources: list[dict]):
        self.redis_client.set(
            f"{SESSION_SOURCES_KEY_PREFIX}{str(session_id)}",
            json.dumps(sources),
            ex=500
        )

    def delete(self, session_id: UUID):
        self.redis_client.delete(f"{SESSION_KEY_PREFIX}{str(session_id)}")
