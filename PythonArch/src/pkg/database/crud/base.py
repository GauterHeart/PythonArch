from abc import ABC
from typing import Any


class CrudABC(ABC):
    async def create(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    async def fetch(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    async def delete(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()


class CrudSyncABC(ABC):
    def create(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    def get(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    def fetch(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    def delete(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()
