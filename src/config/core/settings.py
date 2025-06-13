from pydantic import BaseModel
from pydantic_settings import BaseSettings

import os


class DataBaseSettings(BaseModel):
    """Class with database settings params"""
    url: str = os.getenv('DATABASE_URL')
    echo: bool = os.getenv('DATABASE_ECHO') == "true"

class TokenSettings(BaseModel):
    """Class with token settings params"""
    algorithm: str = os.getenv('TOKEN_ALGORITHM')
    secret_key: str = os.getenv('SECRET_KEY')
    expires_in: int = int(os.getenv('TOKEN_EXPIRES'))
    token_type: str = os.getenv('TOKEN_TYPE')
    token_header: str = "Authorization"
    cookie_auth_key: str = "token"
    password_to_create_user: str = os.getenv("PASSWORD_TO_CREATE_USER")

class RouterSettings(BaseModel):
    auth_tag: str = "Auth"
    auth_prefix: str = "/auth"

class Settings(BaseSettings):
    """Main settings class with all settings classes"""
    database_settings: DataBaseSettings = DataBaseSettings()
    token_settings: TokenSettings = TokenSettings()
    router_settings: RouterSettings = RouterSettings()

settings = Settings()