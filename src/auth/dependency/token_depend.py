from src.auth.utils.token import PyJWTTokenHandler
from src.config.core.settings import settings


def get_pyjwt_token_handler() -> PyJWTTokenHandler:
    return PyJWTTokenHandler(
        secret_key=settings.token_settings.secret_key,
        algorithm=settings.token_settings.algorithm,
    )