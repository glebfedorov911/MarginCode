from src.auth.utils.hasher import PasswordHasher


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()