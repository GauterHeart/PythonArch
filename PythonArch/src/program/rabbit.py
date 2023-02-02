import asyncio

from src.controller.v1.rabbit import LoggerRabbitControllerV1
from src.pkg.arch import AppABC

from .app import BaseApp


class RabbitAddressV1App(BaseApp, AppABC):
    name = "rabbit_logger_v1"

    def __init_rabbit(self) -> LoggerRabbitControllerV1:
        return LoggerRabbitControllerV1(
            host=self._config.RABBIT_HOST,
            port=self._config.RABBIT_PORT,
            username=self._config.RABBIT_USER,
            password=self._config.RABBIT_PASSWORD,
            queue_name=self._config.RABBIT_QUEUE_LOGGER,
            handler=self._logger_handler,
            status_handler=self._rabbit_status_handler,
        )

    def run(self) -> None:
        asyncio.run(self.__init_rabbit().run())
