from contextlib import contextmanager
from typing import Generator, List, Optional

import psycopg2.extras
from psycopg2 import pool
from pydantic import SecretStr


class SyncPostgresql:
    """Sync postgresql driver."""

    def __init__(
        self, host: str, port: int, user: str, password: SecretStr, db: str
    ) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.__pool: Optional[pool.SimpleConnectionPool] = None

    @contextmanager
    def _create_connector(self) -> Generator:
        if self.__pool is None:
            self.__pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=20,
                user=self.__user,
                password=self.__password.get_secret_value(),
                host=self.__host,
                port=self.__port,
                database=self.__db,
            )
        conn = self.__pool.getconn()
        try:
            yield conn
        finally:
            self.__pool.putconn(conn)

    def execute(self, query: str, arg: dict) -> None:
        with self._create_connector() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(query, arg)
            conn.commit()

    def get(self, query: str, arg: dict) -> dict:
        with self._create_connector() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(query, arg)
            effect = cur.fetchone()
            return effect

    def fetch(self, query: str, arg: dict) -> List[dict]:
        with self._create_connector() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(query, arg)
            effect = cur.fetchall()
            return effect

    def fetch_without_factory(self, query: str, arg: dict) -> List[dict]:
        with self._create_connector() as conn:
            cur = conn.cursor()
            cur.execute(query, arg)
            effect = cur.fetchall()
            return effect
