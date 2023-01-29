from cryptography.fernet import Fernet

from src.config import get_settings
from src.core.auth import AuthService
from src.core.initer import IniterService
from src.core.rabbit.status import RabbitStatusHandler
from src.crud import FactoryCrud
from src.pkg.database import Postgresql, SyncPostgresql
from src.pkg.database.redis import RedisAsync, RedisSSL
from src.pkg.rabbit import RabbitPublisher


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
    _rabbit_status_handler = RabbitStatusHandler()

    _auth_service = AuthService(
        crud_p=_crud.init_postgres_crud(),
        crud_r=_crud.init_redis_crud(),
        fernet=_fernet,
    )
