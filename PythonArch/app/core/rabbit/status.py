from aio_pika.abc import AbstractMessage

from app.pkg.exception import BaseExceptionHandler
from app.pkg.rabbit import RabbitStatusHandlerABC


class RabbitStatusHandler(RabbitStatusHandlerABC):
    async def func_200(self, msg: AbstractMessage) -> None:
        ...

    async def func_400(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None:
        ...

    async def func_500(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None:
        ...
