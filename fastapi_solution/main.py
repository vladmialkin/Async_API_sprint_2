from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from fastapi_solution.src.api.v1 import films, genres, persons
from fastapi_solution.src.core import config
from fastapi_solution.src.db import elastic, redis


@asynccontextmanager
async def lifespan(app_):
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    lifespan=lifespan,
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения"
)

add_pagination(app)


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
