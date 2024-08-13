from typing import Any, Protocol


class Storage(Protocol):
    async def get(self, *args, **kwargs) -> Any:
        """Получить объект по ключу"""

    async def list(self, *args, **kwargs) -> list[Any]:
        """Получить список объектов."""

    async def add(self, *args, **kwargs) -> None:
        """Добавить объект по ключу"""
