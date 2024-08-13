from typing import Annotated

from fastapi import Depends

from ..repository.person import PersonRepository as _PersonRepository
from ..repository.person import get_person_repository

PersonRepository = Annotated[_PersonRepository, Depends(get_person_repository)]
