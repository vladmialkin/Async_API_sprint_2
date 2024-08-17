from fastapi import APIRouter, HTTPException, status

from ...repository.elasticsearch import ESRepository
from ...repository.redis import RedisRepository
from ...service.film import FilmService
from ..deps import ESConnection, RedisConnection
from ..v2.schemas.film import FilmSchema

router = APIRouter()


@router.get("")
async def get_all(
    es_conn: ESConnection,
    redis_conn: RedisConnection,
    page_size: int,
    page_number: int,
    sort: str | None = None,
    genre: str | None = None,
) -> list[FilmSchema]:
    service = FilmService(
        storage=ESRepository(es_conn),
        cache=RedisRepository(redis_conn, 60 * 5),
    )
    return await service.get_all(sort, genre, page_size, page_number)


@router.get("/search")
async def search(
    es_conn: ESConnection,
    redis_conn: RedisConnection,
    page_size: int,
    page_number: int,
    title: str,
) -> list[FilmSchema]:
    service = FilmService(
        storage=ESRepository(es_conn),
        cache=RedisRepository(redis_conn, 60 * 5),
    )
    return await service.search(title, page_size, page_number)


@router.get("/{film_id}")
async def details(
    es_conn: ESConnection, redis_conn: RedisConnection, film_id: str
) -> FilmSchema:
    service = FilmService(
        storage=ESRepository(es_conn),
        cache=RedisRepository(redis_conn, 60 * 5),
    )

    film = await service.get(key=film_id)

    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Film not found"
        )

    return film
