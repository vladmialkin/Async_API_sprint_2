from uuid import UUID

from ...v2.schemas.base import BaseSchema


class PersonFilmSchema(BaseSchema):
    id: UUID
    roles: list[str]


class PersonSchema(BaseSchema):
    id: UUID
    full_name: str
    films: list[PersonFilmSchema]
