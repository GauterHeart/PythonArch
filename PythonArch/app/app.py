from typing import List, Optional, Type

from app.config.config import get_settings
from app.pkg.arch.exception import ProgramException
from app.pkg.arch.program import AppABC
from app.program import HttpApp, RabbitTokenCreateV1App


class App:

    _config = get_settings()

    def __program(self) -> List[Type[AppABC]]:
        return [HttpApp, RabbitTokenCreateV1App]

    def __app(self) -> Optional[AppABC]:
        for p in self.__program():
            if p.name == self._config.PROGRAM:
                return p()

        return None

    def run(self) -> AppABC:
        app = self.__app()
        if app is None:
            raise ProgramException()

        return app


app = App().run()
