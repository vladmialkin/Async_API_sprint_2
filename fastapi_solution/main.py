import asyncio

import backoff
from elasticsearch import AsyncElasticsearch
from elasticsearch import ConnectionError as ElasticConError
from elasticsearch import ConnectionTimeout as ElasticConnectionTimeout
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from redis import ConnectionError as RedisConError
from redis import TimeoutError as RedisTimeoutError
from redis.asyncio import Redis

from fastapi_solution.src.api.v1 import films, genres, persons
from fastapi_solution.src.api.v2 import film as films_v2
from fastapi_solution.src.api.v2 import genre as genres_v2
from fastapi_solution.src.api.v2 import person as persons_v2
from fastapi_solution.src.core import config
from fastapi_solution.src.core.config import MAX_TRIES
from fastapi_solution.src.db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
)

add_pagination(app)


@backoff.on_exception(
    backoff.expo, (RedisConError, RedisTimeoutError), max_tries=MAX_TRIES
)
async def setup_redis():
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    await redis.redis.ping()


@backoff.on_exception(
    backoff.expo, (ElasticConError, ElasticConnectionTimeout), max_tries=MAX_TRIES
)
async def setup_elasticsearch():
    elastic.es = AsyncElasticsearch(
        hosts=[f"http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"]
    )
    await elastic.es.ping()


@app.on_event("startup")
async def startup():
    await asyncio.gather(setup_redis(), setup_elasticsearch())


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(persons_v2.router, prefix="/api/v2/persons", tags=["persons"])
app.include_router(films_v2.router, prefix="/api/v2/films", tags=["films"])
app.include_router(genres_v2.router, prefix="/api/v2/genres", tags=["genres"])
