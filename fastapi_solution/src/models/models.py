from typing import Optional

from pydantic import BaseModel


class FilmRequest(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    creation_date: Optional[str]
    genres: list[dict[str, Optional[str]]]
    description: Optional[str]
    file_path: Optional[dict]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[dict[str, str]]
    actors: list[dict[str, str]]
    writers: list[dict[str, str]]


class FilmFullResponse(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    creation_date: Optional[str]
    genres: list[dict[str, Optional[str]]]
    description: Optional[str]
    directors: list[dict[str, str]]
    actors: list[dict[str, str]]
    writers: list[dict[str, str]]


class FilmResponse(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class Genre(BaseModel):
    id: str
    name: str
    description: str | None


class Person(BaseModel):
    id: str
    full_name: str
    films: list[dict]


class Actor(BaseModel):
    id: str
    full_name: str


class Director(BaseModel):
    id: str
    full_name: str


class Writer(BaseModel):
    id: str
    full_name: str
