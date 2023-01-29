from fastapi import APIRouter

from src.core.auth import AuthService
from src.pkg.arch import HttpControllerABC


class HttpControllerV1(HttpControllerABC):
    router = APIRouter(prefix="/v1")

    def __init__(self, auth_service: AuthService) -> None:
        self.__auth_service = auth_service
        self._init_router()

    def _init_router(self) -> None:
        ...