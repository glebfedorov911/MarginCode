from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from typing import Callable

from src.config.core.settings import settings


class TokenToHeaderMiddleware(BaseHTTPMiddleware):
    auth_key: str = settings.token_settings.cookie_auth_key
    token_type: str = settings.token_settings.token_type
    token_header: str = settings.token_settings.token_header

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        token = request.cookies.get(self.auth_key)

        if token:
            request.scope["headers"] = [
                (key, value)
                if key != self.token_header.lower().encode()
                else (key, f"{self.token_type} {token}".encode())
                for key, value in request.scope["headers"]
            ]

            if not any(key == self.token_header.lower().encode() for key, _ in request.scope["headers"]):
                request.scope["headers"].append((self.token_header.lower().encode(), f"{self.token_type} {token}".encode()))

        return await call_next(request)