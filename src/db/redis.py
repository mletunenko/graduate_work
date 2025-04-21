import logging

from redis import RedisError
from redis.asyncio import Redis

from core.config import settings

logger = logging.getLogger(__name__)

__redis_client__ = Redis(host=settings.redis.host, port=settings.redis.port)


async def get_redis_connection() -> Redis | None:
    try:
        global __redis_client__
        return __redis_client__
    except RedisError as e:
        logger.error(f"Ошибка подключения к Redis: {e}")
        raise
