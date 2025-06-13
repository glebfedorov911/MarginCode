from enum import Enum


class UserServiceExceptionMessages(Enum):
    """Enum with exception for user service"""

    BAD_SECRET = "Incorrect secret to create user"
    BAD_PASSWORD = "Incorrect password to login"
    CREDENTIAL = "Could not validate credentials"

class UserServiceException(Exception):
    """Exception for user service"""

    def __init__(self, message: str, code: int = 405):
        super().__init__(message)
        self.code = code