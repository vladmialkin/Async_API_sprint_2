from typing import Annotated
from ..storage.es import ESStorage as _ESStorage, get_es_storage
from ..storage.redis import RedisStorage as _RedisStorage, get_redis_storage
from fastapi import Depends


ESStorage = Annotated[_ESStorage, Depends(get_es_storage)]
RedisStorage = Annotated[_RedisStorage, Depends(get_redis_storage)]

