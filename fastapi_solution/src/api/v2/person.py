from fastapi import APIRouter, HTTPException, status
from ..v2.schemas.person import PersonSchema
from ..deps import PersonRepository


router = APIRouter()


@router.get("/{person_id}")
async def details(repository: PersonRepository, person_id: str) -> PersonSchema:
    person = await repository.get(person_id)

    if not person:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")

    return person


@router.get("/search")
async def search(
    repository: PersonRepository,
    name: str,
    page_size: int = 50,
    page_number: int = 1,
) -> list[PersonSchema]:
    return await repository.list(name=name, page_size=page_size, page_number=page_number)