from typing import List, Optional, Type

from src.config.config import get_settings
from src.pkg.arch.exception import ProgramException
from src.pkg.arch.program import AppABC
from src.program import HttpApp

__all__ = ["app"]


class App:
    _config = get_settings()

    def __program(self) -> List[Type[AppABC]]:
        return [HttpApp]

    def __app(self) -> Optional[AppABC]:
        for p in self.__program():
            if p.name == self._config.PROGRAM:
                return p()

        return None

    def setup(self) -> AppABC:
        app = self.__app()
        if app is None:
            raise ProgramException()

        return app


app = App().setup()
