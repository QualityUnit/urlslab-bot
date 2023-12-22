import redis
from redis import Redis

from backend.core.config import config

redis_client: Redis = redis.from_url(config.REDIS_URL)
