from fastapi import APIRouter

from src.controller.v1.handler import LoggerHandler
from src.core.auth import AuthService
from src.pkg.arch import HttpControllerABC

from .logger import LoggerHttpController


class HttpControllerV1(HttpControllerABC):
    router = APIRouter(prefix="/v1")

    def __init__(
        self, auth_service: AuthService, logger_handler: LoggerHandler
    ) -> None:
        self._auth_service = auth_service
        self._logger_handler = logger_handler
        self._init_router()

    def _init_router(self) -> None:
        self.router.include_router(
            router=LoggerHttpController(handler=self._logger_handler).router
        )
