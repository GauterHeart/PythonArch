from src.controller.v1.schema import logger


class LoggerHandler:
    async def create(self, spell: logger.LoggerCreateSchema) -> None:
        ...
