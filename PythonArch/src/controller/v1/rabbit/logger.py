from pydantic import SecretStr

from src.controller.v1.handler import LoggerHandler
from src.controller.v1.schema import logger
from src.core.rabbit import RabbitStatusHandler
from src.pkg.rabbit import RabbitConsumer


class LoggerRabbitControllerV1(RabbitConsumer):
    def __init__(
        self,
        handler: LoggerHandler,
        host: str,
        port: int,
        username: str,
        password: SecretStr,
        queue_name: str,
        status_handler: RabbitStatusHandler,
    ):

        super().__init__(
            host=host,
            password=password,
            username=username,
            port=port,
            queue_name=queue_name,
            status_handler=status_handler,
        )

        self.__handler = handler

    async def run(self) -> None:
        await self._broker(
            func=self.__handler.create,
            model=logger.LoggerCreateRabbitSchema,
        )
