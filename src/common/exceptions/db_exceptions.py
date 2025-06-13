from enum import Enum


class DataBaseExceptionMessages(Enum):
    """Enum with exception from database"""

    NOT_FOUND_BY = "Not found record with data = %s in model %s"

class NotFoundException(Exception):
    """Exception for not found record"""

    def __init__(self, message: str, code: int = 404):
        super().__init__(message)
        self.code = code