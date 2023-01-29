from typing import Optional

from src.model import ClientModel
from src.pkg.database import Postgresql
from src.pkg.database.crud import CrudABC


class ClientCRUD(CrudABC):
    def __init__(self, cursor: Postgresql) -> None:
        self.__cursor = cursor

    async def get(self, public_key: str) -> Optional[ClientModel]:
        query = """
            select * from client where public_key = $1;
        """

        effect = await self.__cursor.fetchrow(query, public_key)
        if effect is not None:
            return ClientModel(**effect)

        return effect
