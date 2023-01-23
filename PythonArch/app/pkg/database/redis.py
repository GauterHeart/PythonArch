from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Optional

import aioredis
from pydantic import SecretStr

__all__ = ["Redis", "RedisAsync", "RedisSSL"]


class Redis(ABC):
    @abstractmethod
    async def set(self, name: str, value: str, expire: Optional[int] = None) -> None:
        ...

    @abstractmethod
    async def get(self, name: str) -> str:
        ...

    @abstractmethod
    async def delete(self, name: str) -> None:
        ...

    @abstractmethod
    async def hset(self, name: str, key: str, value: str) -> None:
        ...

    @abstractmethod
    async def hget(self, name: str, key: str) -> str:
        ...

    @abstractmethod
    async def hgetall(self, name: str) -> Dict[str, str]:
        ...


class RedisAsync(Redis):

    __connector: Optional[aioredis.Redis] = None

    def __init__(
        self, host: str, port: int, user: str, password: SecretStr, db: str
    ) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.__pool = aioredis.ConnectionPool.from_url(
            self.__create_dsn(), max_connections=10
        )

    def __create_dsn(self) -> str:
        return (
            f"redis://{self.__user}:{self.__password.get_secret_value()}"
            + f"@{self.__host}:{self.__port}/{self.__db}"
        )

    @asynccontextmanager
    async def _create_connector(self) -> AsyncGenerator[aioredis.Redis, None]:
        if self.__connector is None:
            self.__connector = aioredis.Redis(connection_pool=self.__pool)

        yield self.__connector

    async def set(self, name: str, value: str, expire: Optional[int] = None) -> None:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.set(name=name, value=value, ex=expire)

    async def get(self, name: str) -> str:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                return await conn.get(name=name)

    async def delete(self, name: str) -> None:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.delete(name)

    async def hset(self, name: str, key: str, value: str) -> None:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                return await conn.hset(name=name, key=key, value=value)

    async def hget(self, name: str, key: str) -> str:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                return await conn.hget(name=name, key=key)

    async def hgetall(self, name: str) -> Dict[str, str]:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                return await conn.hgetall(name=name)


class RedisSSL(Redis):
    __connection: Optional[aioredis.StrictRedis] = None

    def __init__(
        self, host: str, port: int, user: str, password: SecretStr, db: str
    ) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.__connection = self.__make_connection()

    def __make_connection(self) -> aioredis.StrictRedis:
        if self.__connection is None:
            return aioredis.StrictRedis(
                host=self.__host,
                port=self.__port,
                username=self.__user,
                password=self.__password.get_secret_value(),
                db=self.__db,
                ssl=True,
            )
        return self.__connection

    async def set(self, name: str, value: str, expire: Optional[int] = None) -> None:
        redis = self.__make_connection()
        await redis.set(name=name, value=value, ex=expire)

    async def get(self, name: str) -> str:
        redis = self.__make_connection()
        return await redis.get(name)

    async def delete(self, name: str) -> None:
        redis = self.__make_connection()
        await redis.delete(name)

    async def hset(self, name: str, key: str, value: str) -> None:
        redis = self.__make_connection()
        return await redis.hset(name=name, key=key, value=value)

    async def hget(self, name: str, key: str) -> str:
        redis = self.__make_connection()
        return await redis.hget(name=name, key=key)

    async def hgetall(self, name: str) -> Dict[str, str]:
        redis = self.__make_connection()
        return await redis.hgetall(name=name)
