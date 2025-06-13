from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import jwt

from src.common.exceptions.token_exceptions import (
    TokenException,
    TokenEncodeExceptionMessages, TokenDecodeExceptionMessages
)

class TokenHandler(ABC):

    @abstractmethod
    def encode(self, payload: dict, expires: int) -> str:
        """
        Method for encode
        :param payload: dict with data for encode
        :param expires: lifetime of token
        :return: token
        """

    @abstractmethod
    def decode(self, token: str) -> dict:
        """Method for decode"""

class PyJWTTokenHandler(TokenHandler):
    """Class with pyjwt token handler"""

    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode(self, payload: dict, expires: int) -> str:
        """
        Method for encode
        :param payload: dict with data for encode
        :param expires: lifetime of token
        :return: token
        """
        encoder = PyJWTEncoder(self.secret_key, self.algorithm, expires)
        return encoder.encode(payload)

    def decode(self, token: str) -> dict:
        """Method for decode"""
        decoder = PyJWTDecoder(self.secret_key, self.algorithm)
        return decoder.decode(token)

class PyJWTEncoder:
    """Class with pyjwt token encoder"""

    def __init__(self, secret_key: str, algorithm: str, expires_hours: int) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_hours = expires_hours

    def encode(self, payload: dict) -> str:
        """
        Method to encode payload
        :param payload: data to encode
        :return: token
        """
        try:
            exp = self._calculate_expires_time()
            payload.update({"exp": exp})
            return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        except jwt.exceptions.PyJWTError as e:
            raise TokenException(TokenEncodeExceptionMessages.ENCODED.value)

    def _calculate_expires_time(self) -> datetime:
        """
        Method to calculate expires time
        :return: date
        """
        return datetime.now() + timedelta(hours=self.expires_hours)

class PyJWTDecoder:
    """Class with pyjwt token decoder"""

    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode(self, token: str) -> dict:
        """
        Method for decode
        :param token: string with token
        :return: dict with data
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenException(TokenDecodeExceptionMessages.EXPIRED_TOKEN.value)
        except jwt.exceptions.InvalidTokenError:
            raise TokenException(TokenDecodeExceptionMessages.INVALID_TOKEN.value)
        except jwt.exceptions.PyJWTError:
            raise TokenException(TokenDecodeExceptionMessages.DECODED.value)