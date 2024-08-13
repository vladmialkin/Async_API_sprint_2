from typing import Annotated

from fastapi import Depends

from ..storage.es import ESStorage as _ESStorage
from ..storage.es import get_es_storage
from ..storage.redis import RedisStorage as _RedisStorage
from ..storage.redis import get_redis_storage

ESStorage = Annotated[_ESStorage, Depends(get_es_storage)]
RedisStorage = Annotated[_RedisStorage, Depends(get_redis_storage)]
