import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.controller.v1.http import HttpControllerV1
from src.core.initer import IniterService
from src.pkg.arch import AppABC
from src.pkg.database.redis import RedisAsync, RedisSSL
from src.pkg.exception.base import BaseExceptionHandler
from src.program.app import BaseApp


class HttpApp(BaseApp, AppABC):
    """Http server object."""

    name = "http"

    __app = FastAPI()

    def __init__(self) -> None:
        self.__redis_connection()
        self.__reg_controller()
        self.__reg_middleware()

    def __redis_connection(self) -> None:
        IniterService.cursor_r = (
            RedisSSL(
                host=self._config.REDIS_HOST,
                port=self._config.REDIS_PORT,
                user=self._config.REDIS_USER,
                password=self._config.REDIS_PASSWORD,
                db=self._config.REDIS_DB,
            )
            if self._config.REDIS_SSL is True
            else RedisAsync(
                host=self._config.REDIS_HOST,
                port=self._config.REDIS_PORT,
                user=self._config.REDIS_USER,
                password=self._config.REDIS_PASSWORD,
                db=self._config.REDIS_DB,
            )
        )

        IniterService.health_connection_redis()

    def __init_controller_v1(self) -> HttpControllerV1:
        return HttpControllerV1(
            auth_service=self._auth_service, logger_handler=self._logger_handler
        )

    @staticmethod
    @__app.exception_handler(BaseExceptionHandler)
    async def validation_exception_handler(
        request: Request, exc: BaseExceptionHandler
    ) -> JSONResponse:
        _ = request
        return JSONResponse(exc.detail, status_code=exc.status_code)

    def __reg_controller(self) -> None:
        self.__app.include_router(router=self.__init_controller_v1().router)

    def __reg_middleware(self) -> None:
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def __call__(self) -> FastAPI:
        return self.__app

    def run(self) -> None:
        uvicorn.run(
            "main:app",
            host=self._config.HOST,
            port=self._config.PORT,
            workers=self._config.WORKER,
            factory=True,
            reload=self._config.RELOAD,
        )
