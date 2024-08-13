from typing import Any

from elasticsearch import AsyncElasticsearch

from ..storage.deps import ElasticClient


class ESStorage:
    def __init__(self, es_conn: AsyncElasticsearch, index: str) -> None:
        self._conn = es_conn
        self.index = index

    async def get(self, key: str) -> Any:
        return await self._conn.get(index=self.index, id=key)

    async def list(self, page_size: int, page_number: int, **kwargs) -> list[Any]:
        query: dict[str, Any] = {"query": {"bool": {"must": []}}}
        query["from"] = (page_number - 1) * page_size
        query["size"] = page_size

        query["query"]["bool"]["must"].append(kwargs)

        return await self._conn.search(index=self.index, query=query)

    async def add(self) -> None:
        raise NotImplementedError


def get_es_storage(es_conn: ElasticClient, index: str) -> ESStorage:
    return ESStorage(es_conn, index)
