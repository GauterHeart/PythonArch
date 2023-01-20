from app.pkg.database import Postgresql
from app.pkg.database.crud import CrudABC


class TokenCRUD(CrudABC):
    def __init__(self, cursor: Postgresql) -> None:
        self.__cursor = cursor

    async def create(self, token: str) -> None:
        query = """
            insert in token(name) values($1);
        """
        await self.__cursor.fetchrow(query, token)
