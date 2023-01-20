from fastapi import APIRouter

from app.controller.v1.handler import TokenHandlerV1
from app.core.auth import AuthService
from app.pkg.arch import HttpControllerABC

from .token import TokenHttpController


class HttpControllerV1(HttpControllerABC):
    router = APIRouter(prefix="/v1")

    def __init__(
        self, auth_service: AuthService, token_handler: TokenHandlerV1
    ) -> None:
        self.__auth_service = auth_service
        self.__token_handler = token_handler
        self._init_router()

    def _init_router(self) -> None:
        self.router.include_router(
            router=TokenHttpController(handler=self.__token_handler).router,
        )
