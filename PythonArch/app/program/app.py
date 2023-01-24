from cryptography.fernet import Fernet

from app.config import get_settings
from app.controller.v1.handler import TokenHandlerV1
from app.core.auth import AuthService
from app.core.initer import IniterService
from app.core.rabbit.status import RabbitStatusHandler
from app.crud import FactoryCrud
from app.pkg.database import Postgresql, SyncPostgresql
from app.pkg.database.redis import RedisAsync, RedisSSL
from app.pkg.rabbit import RabbitPublisher


class BaseApp:
    """Base init object."""

    _config = get_settings()

    _fernet = Fernet(_config.CRYPT_KEY)

    IniterService.cursor_p = SyncPostgresql(
        host=_config.POSTGRES_HOST,
        db=_config.POSTGRES_DB,
        password=_config.POSTGRES_PASSWORD,
        port=_config.POSTGRES_PORT,
        user=_config.POSTGRES_USER,
    )
    IniterService.health_connection_postgresql()

    _crud = FactoryCrud(
        Postgresql(
            db=_config.POSTGRES_DB,
            host=_config.POSTGRES_HOST,
            port=_config.POSTGRES_PORT,
            password=_config.POSTGRES_PASSWORD,
            user=_config.POSTGRES_USER,
        ),
        redis_cursor=RedisSSL(
            host=_config.REDIS_HOST,
            port=_config.REDIS_PORT,
            user=_config.REDIS_USER,
            password=_config.REDIS_PASSWORD,
            db=_config.REDIS_DB,
        )
        if _config.REDIS_SSL is True
        else RedisAsync(
            host=_config.REDIS_HOST,
            port=_config.REDIS_PORT,
            user=_config.REDIS_USER,
            password=_config.REDIS_PASSWORD,
            db=_config.REDIS_DB,
        ),
    )
    _rabbit_publisher = RabbitPublisher(
        dsn=f"amqp://{_config.RABBIT_USER}:{_config.RABBIT_PASSWORD}@"
        + f"{_config.RABBIT_HOST}:{_config.RABBIT_PORT}"
    )
    _token_handler_v1 = TokenHandlerV1(crud_p=_crud.init_postgres_crud())
    _rabbit_status_handler = RabbitStatusHandler()

    _auth_service = AuthService(
        crud_p=_crud.init_postgres_crud(),
        crud_r=_crud.init_redis_crud(),
        fernet=_fernet,
    )
