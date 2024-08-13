from functools import lru_cache

from ..models.models import Person
from ..repository.deps import ESStorage, RedisStorage
from ..repository.interface import Repository


class PersonRepository(Repository[Person]):
    def __init__(self, storage: ESStorage, cache: RedisStorage) -> None:
        self._storage = storage
        self._cache = cache

    async def get(self, key: str) -> Person:
        return await self._cache.get(
            slug="person/get", key=key
        ) or await self._storage.get(key)

    async def list(self, page_size: int, page_number: int, **kwargs) -> list[Person]:
        data = await self._storage.list(page_size, page_number, **kwargs)
        await self._cache.add(
            slug="person/search",
            value=data,
            page_size=page_size,
            page_number=page_number,
            **kwargs
        )

        return data


@lru_cache(maxsize=1)
def get_person_repository(storage: ESStorage, cache: RedisStorage) -> PersonRepository:
    return PersonRepository(storage, cache)
