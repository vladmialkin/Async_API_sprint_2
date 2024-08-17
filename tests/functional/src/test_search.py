import asyncio

import pytest

from tests.functional.settings import test_settings





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


@pytest.mark.asyncio
async def test_get_film_by_redis(generate_es_data_for_persons_index, es_write_data, make_get_request, del_all_redis_keys):
    response = await aiohttp_client.post(url="/film", params=film_json)
    assert response.status_code == 201
    assert response.json() == {'message': 'Film created successfully!'}