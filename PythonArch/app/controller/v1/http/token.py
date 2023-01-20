from fastapi import APIRouter, Query

from app.controller.v1.handler import TokenHandlerV1
from app.controller.v1.schema import token
from app.pkg.arch import HttpControllerABC


class TokenHttpController(HttpControllerABC):
    router = APIRouter(prefix="/token")

    def __init__(self, handler: TokenHandlerV1) -> None:
        self.__handler = handler
        self._init_router()

    def _init_router(self) -> None:
        self.router.add_api_route(path="/", endpoint=self.__get, methods=["Get"])

    async def __get(self, token: str = Query(max_length=64)) -> None:
        print(token)

    async def __create(self, spell: token.TokenCreateSchema) -> None:
        ...
