from fastapi import APIRouter, HTTPException, status

from ...repository.elasticsearch import ESRepository
from ...repository.redis import RedisRepository
from ...service.genre import GenreService
from ..deps import ESConnection, RedisConnection
from ..v2.schemas.genre import GenreSchema

router = APIRouter()


@router.get("/{genre_id}")
async def details(
    es_conn: ESConnection, redis_conn: RedisConnection, genre_id: str
) -> GenreSchema:
    service = GenreService(
        storage=ESRepository(es_conn),
        cache=RedisRepository(redis_conn, ttl=60 * 5),
    )

    genre = await service.get(key=genre_id)

    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found"
        )

    return genre


@router.get("")
async def get_all(
    es_conn: ESConnection, redis_conn: RedisConnection
) -> list[GenreSchema]:
    service = GenreService(
        storage=ESRepository(es_conn),
        cache=RedisRepository(redis_conn, ttl=60 * 5),
    )

    return await service.get_all()
