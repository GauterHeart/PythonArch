import asyncio

from app.controller.v1.rabbit.token import TokenCreateV1RabbitController
from app.pkg.arch import AppABC
from app.program.app import BaseApp


class RabbitTokenCreateV1App(BaseApp, AppABC):
    name = "rabbit_token_create_v1"

    def __init_rabbit(self) -> TokenCreateV1RabbitController:
        return TokenCreateV1RabbitController(
            host=self._config.RABBIT_HOST,
            port=self._config.RABBIT_PORT,
            username=self._config.RABBIT_USER,
            password=self._config.RABBIT_PASSWORD,
            queue_name=self._config.RABBIT_QUEUE_TOKEN_CREATE,
            handler=self._token_handler_v1,
            status_handler=self._rabbit_status_handler,
        )

    def run(self) -> None:
        asyncio.run(self.__init_rabbit().run())
