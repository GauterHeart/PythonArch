from fastapi import APIRouter

from src.controller.v1.handler import LoggerHandler
from src.controller.v1.schema import logger
from src.pkg.arch import HttpControllerABC

__all__ = ["LoggerHttpController"]


class LoggerHttpController(HttpControllerABC):
    router = APIRouter(prefix="/log")

    def __init__(self, handler: LoggerHandler) -> None:
        self.__handler = handler
        self._init_router()

    def _init_router(self) -> None:
        self.router.add_api_route(
            path="/create", endpoint=self.__create, methods=["POST"]
        )

    async def __create(self, spell: logger.LoggerCreateHttpSchema) -> None:
        await self.__handler.create(spell=spell)
