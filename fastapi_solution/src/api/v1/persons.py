import logging
from http import HTTPStatus
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate

from ...models.models import Person
from ...services.person_service import PersonService, get_person_service

router = APIRouter()

log = logging.getLogger("main")


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Поиск персоны по id",
    description="Получение информации по id",
    response_description="Полная информация по персоне",
)
async def genre_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> Person:
    log.info(f"Получение информации по персоне с id: {person_id} ...")
    person = await person_service.get_by_id(person_id)

    if not person:
        log.info(f"Персона с id: {person_id} не найдена.")
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")

    log.info(f"Информация по персоне с id: {person_id} получена.")
    return person


@router.get(
    "",
    summary="Список персон",
    description="Список персон с пагинацией",
    response_description="Информация по персонам",
)
async def persons(
    person_service: PersonService = Depends(get_person_service),
    sort_by: Optional[Literal["writer", "director", "actor"]] = Query(None),
) -> Page[Person]:
    log.info("Получение персон ...")
    persons_list = await person_service.get_all_persons()

    if not persons:
        log.info(f"Персон не найдено.")
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Persons not found"
        )

    if sort_by is not None:
        # получение только тек персон, роли которых совпадают с выбранным
        persons_list = [
            person
            for person in persons_list
            if any(role == sort_by for film in person.films for role in film["roles"])
        ]

    log.info(f"Получено {len(persons_list)} персон.")
    return paginate(persons_list)
