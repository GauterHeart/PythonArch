from ...exception.base import BaseExceptionHandler


class RabbitModelValidatorException(BaseExceptionHandler):
    status_code = 422
    detail = "Model is not valid"
