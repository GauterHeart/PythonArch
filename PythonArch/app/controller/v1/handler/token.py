from app.controller.v1.schema import token
from app.crud import PostgresCRUD
from app.pkg.exception import IdAlreadyExistException


class TokenHandlerV1:
    def __init__(self, crud_p: PostgresCRUD) -> None:
        self.__crud_p = crud_p

    async def create(self, spell: token.TokenCreateSchema) -> None:
        raise IdAlreadyExistException()
        # await self.__crud_p.token.create(token=spell.token)
