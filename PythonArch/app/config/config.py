import argparse
from enum import Enum
from functools import lru_cache
from typing import Optional

from dotenv import find_dotenv
from pydantic import BaseSettings, SecretStr

__all__ = ["get_settings"]


class RunType(Enum):
    DEV = "dev"
    PROD = "prod"

    def __str__(self) -> str:
        return self.value


class RunProgram(Enum):
    HTTP = "http"
    RABBIT_TOKEN_CREATE_V1 = "rabbit_token_create_v1"

    def __str__(self) -> str:
        return self.value


class _Setting(BaseSettings):
    class Config:
        env_file: str
        env_file_encoding = "utf-8"


class Setting(_Setting):
    # server
    HOST: str
    PORT: int
    WORKER: int
    RELOAD: bool

    # Postgres
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: str
    REDIS_USER: str
    REDIS_PASSWORD: SecretStr

    # Rabbit
    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USER: str
    RABBIT_PASSWORD: SecretStr
    RABBIT_QUEUE_TOKEN_CREATE: str

    # Crypt
    CRYPT_KEY: str

    # program
    PROGRAM: Optional[str] = None


# Parsing arg in command line
def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=RunType, type=RunType)
    parser.add_argument("program", choices=RunProgram, type=RunProgram)
    args = parser.parse_args()
    return args


@lru_cache()
def get_settings() -> Setting:
    args = arg_parser()
    type_of_worker = RunType(args.type)
    type_of_program = RunProgram(args.program)
    settings = Setting(
        _env_file=find_dotenv(
            ".prod.env" if type_of_worker.value == "prod" else ".dev.env"
        ),
    )
    settings.PROGRAM = type_of_program.value
    return settings
