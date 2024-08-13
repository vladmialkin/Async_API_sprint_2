from typing import Any
from redis.asyncio import Redis
import pickle
from ..storage.deps import RedisClient


class RedisStorage:
    def __init__(self, redis_conn: Redis, ttl: int) -> None:
        self._conn = redis_conn
        self._ttl = ttl
    
    @classmethod
    def _compute_key(cls, slug: str, **kwargs) -> str:
        return f"{slug}:".join(f"{key}={value}" for key, value in sorted(kwargs.items()))
    
    async def get(self, slug: str, **kwargs) -> Any:
        key = self._compute_key(slug, **kwargs)
        value = await self._conn.get(key)

        if not value:
            return None

        return pickle.loads(value)
        
    async def add(self, slug: str, value: Any, **kwargs) -> None:
        key = self._compute_key(slug, **kwargs)
        await self._conn.set(key, pickle.dumps(value), ex=self._ttl)


def get_redis_storage(redis_conn: RedisClient, ttl: int) -> RedisStorage:
    return RedisStorage(redis_conn, ttl)
