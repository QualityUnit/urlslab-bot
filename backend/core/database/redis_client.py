import redis
from redis import Redis

from core.config import config

redis_client: Redis = redis.from_url(config.REDIS_URL)
