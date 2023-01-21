from pydantic import SecretStr

from app.controller.v1.handler import TokenHandlerV1
from app.controller.v1.schema import token
from app.core.rabbit import RabbitStatusHandler
from app.pkg.rabbit.consumer import RabbitConsumer


class TokenCreateV1RabbitController(RabbitConsumer):
    def __init__(
        self,
        queue_name: str,
        username: str,
        password: SecretStr,
        host: str,
        port: int,
        handler: TokenHandlerV1,
        status_handler: RabbitStatusHandler,
    ) -> None:
        super().__init__(
            queue_name=queue_name,
            username=username,
            password=password,
            host=host,
            port=port,
            status_handler=status_handler,
        )
        self.__handler = handler

    async def run(self) -> None:
        await self._broker(
            func=self.__handler.create,
            model=token.TokenCreateSchema,
        )
