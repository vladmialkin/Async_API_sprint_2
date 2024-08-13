from typing import Annotated

from fastapi import Depends
from ..repository.person import get_person_repository, PersonRepository as _PersonRepository


PersonRepository = Annotated[_PersonRepository, Depends(get_person_repository)]
