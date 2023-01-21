import inspect
from abc import ABC, abstractmethod
from typing import Callable, Type

import aio_pika
import ujson
from aio_pika.abc import AbstractMessage, AbstractRobustConnection
from loguru import logger
from pydantic import BaseModel, SecretStr, parse_obj_as
from pydantic.main import ModelMetaclass

from ..exception import BaseExceptionHandler
from .exception import (
    RabbitInvalidHandlerFunctionException,
    RabbitInvalidModelTypeException,
    RabbitModelValidatorException,
)


class RabbitStatusHandlerABC(ABC):
    @abstractmethod
    async def func_200(self, msg: AbstractMessage) -> None:
        ...

    @abstractmethod
    async def func_400(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None:
        ...

    @abstractmethod
    async def func_500(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None:
        ...


class RabbitConsumer:

    _connection: AbstractRobustConnection

    def __init__(
        self,
        queue_name: str,
        username: str,
        password: SecretStr,
        host: str,
        port: int,
        status_handler: RabbitStatusHandlerABC,
    ) -> None:
        self.__queue_name = queue_name
        self.__username = username
        self.__password = password
        self.__host = host
        self.__port = port
        self.__status_handler = status_handler

    def __create_dsn(self) -> str:
        return (
            f"amqp://{self.__username}:{self.__password.get_secret_value()}@"
            + f"{self.__host}:{self.__port}/"
        )

    def __model_validator(
        self, msg: AbstractMessage, model: Type[BaseModel]
    ) -> BaseModel:
        try:
            effect = parse_obj_as(model, ujson.loads(msg.body.decode("utf-8")))
            logger.info(f"Message: {effect}")
            return effect

        except Exception:
            raise RabbitModelValidatorException()

    async def _broker(self, func: Callable, model: Type[BaseModel]) -> None:
        if len(inspect.signature(func).parameters) != 1:
            raise RabbitInvalidHandlerFunctionException()

        if not isinstance(model, ModelMetaclass):
            raise RabbitInvalidModelTypeException()

        self._connection = await aio_pika.connect_robust(url=self.__create_dsn())
        async with self._connection:

            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(self.__queue_name, auto_delete=False)
            logger.success(f"START: {self.__queue_name}")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process() as msg:
                        try:
                            await func(self.__model_validator(msg=msg, model=model))
                            await self.__status_handler.func_200(msg=msg)
                            logger.success("Successfully")
                        except BaseExceptionHandler as e:
                            if e.status_code >= 500:
                                logger.critical(
                                    f"Status-Code: {e.status_code}, Detail: {e.detail}"
                                )
                                await self.__status_handler.func_500(
                                    msg=msg, exception=e
                                )
                                raise Exception(e.detail)

                            elif e.status_code >= 400:
                                await self.__status_handler.func_400(
                                    msg=msg, exception=e
                                )
                                logger.warning(
                                    f"Status-Code: {e.status_code}, Detail: {e.detail}"
                                )
