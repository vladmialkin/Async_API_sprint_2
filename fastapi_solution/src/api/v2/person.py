from fastapi import APIRouter, HTTPException, status

from ...repository.elasticsearch import ESRepository
from ...repository.redis import RedisRepository
from ...service.person import PersonService
from ..deps import ESConnection, RedisConnection
from ..v2.schemas.person import PersonSchema

router = APIRouter()


@router.get("/search")
async def search(
    es_conn: ESConnection,
    redis_conn: RedisConnection,
    name: str | None = None,
    role: str | None = None,
    film_title: str | None = None,
    page_size: int = 20,
    page_number: int = 1,
) -> list[PersonSchema]:
    service = PersonService(
        ESRepository(es_conn=es_conn),
        RedisRepository(redis_conn=redis_conn, ttl=60 * 5),  # 5 minutes
    )

    return await service.search(
        page_size, page_number, name=name, role=role, film_title=film_title
    )


@router.get("/{person_id}")
async def details(
    es_conn: ESConnection, redis_conn: RedisConnection, person_id: str
) -> PersonSchema:
    service = PersonService(
        ESRepository(es_conn=es_conn),
        RedisRepository(redis_conn=redis_conn, ttl=60 * 5),  # 5 minutes
    )

    person = await service.get(key=person_id)

    if not person:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")

    return person


@router.get("")
async def get_all(
    es_conn: ESConnection, redis_conn: RedisConnection
) -> list[PersonSchema]:
    service = PersonService(
        ESRepository(es_conn=es_conn),
        RedisRepository(redis_conn=redis_conn, ttl=60 * 5),  # 5 minutes
    )

    return await service.get_all()
