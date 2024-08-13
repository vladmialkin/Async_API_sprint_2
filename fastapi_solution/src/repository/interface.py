from abc import ABC, abstractmethod


class Repository[T](ABC):
    @abstractmethod
    async def get(self, key: str) -> T:
        """Получить объект по ключу."""

    @abstractmethod
    async def list(self, *args, **kwargs) -> list[T]:
        """Получить список объектов."""
