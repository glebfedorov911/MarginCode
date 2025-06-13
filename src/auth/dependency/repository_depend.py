from src.auth.repository.user_repository import UserRepository
from src.auth.service.user_create_service import UserCreateService


def get_user_repository() -> UserRepository:
    return UserRepository()