from enum import Enum


class TokenEncodeExceptionMessages(Enum):
    """Enum with exception from token"""

    ENCODED = "Cannot encode this payload"

class TokenDecodeExceptionMessages(Enum):
    """Enum with exception from token"""

    INVALID_TOKEN = "Invalid token"
    EXPIRED_TOKEN = "Token already expired"
    DECODED = "Cannot decode this token"

class TokenException(Exception):
    """Exception for not found record"""

    def __init__(self, message: str, code: int = 422):
        super().__init__(message)
        self.code = code