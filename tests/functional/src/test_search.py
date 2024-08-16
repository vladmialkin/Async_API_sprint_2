import asyncio

import pytest

from tests.functional.settings import test_settings


@pytest.mark.asyncio
async def test_film_by_id(generate_es_data_for_movies_index, es_write_data, make_get_request, del_all_redis_keys):
    films = await generate_es_data_for_movies_index(films_number=10)

    await del_all_redis_keys()
    await es_write_data(test_settings.movies_index_name, films)
    await asyncio.sleep(1)

    film_id = films[0]['id']

    resp = await make_get_request(f'/api/v1/films/{film_id}')
    body = await resp.json()
    status = resp.status

    assert status == 200
    assert body['id'] == film_id

    await del_all_redis_keys()


@pytest.mark.asyncio
async def test_get_all_films(generate_es_data_for_movies_index, es_write_data, make_get_request, del_all_redis_keys):
    films_number = 5

    data = await generate_es_data_for_movies_index(films_number)

    await del_all_redis_keys()
    await es_write_data(test_settings.movies_index_name, data)
    await asyncio.sleep(1)

    resp = await make_get_request(f'/api/v1/films/')
    body = await resp.json()
    status = resp.status

    assert status == 200
    assert len(body['items']) == films_number

    await del_all_redis_keys()


@pytest.mark.asyncio
async def test_person_by_id(generate_es_data_for_persons_index, es_write_data, make_get_request, del_all_redis_keys):
    data = await generate_es_data_for_persons_index(2)

    await del_all_redis_keys()
    await es_write_data(test_settings.persons_index_name, data)
    await asyncio.sleep(1)

    person_id = data[0]['id']
    resp = await make_get_request(f'/api/v1/persons/{person_id}', )

    body = await resp.json()
    status = resp.status

    assert status == 200
    assert body['id'] == person_id

    await del_all_redis_keys()
