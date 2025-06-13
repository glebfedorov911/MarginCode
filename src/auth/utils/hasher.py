import bcrypt


class PasswordHasher:
    """Class for hash password"""

    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Method to hash password
        :param password: password to hash
        :return: hashed password
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def verify_password(password: str, hashed_password: bytes) -> bool:
        """
        Method to verify password
        :param password: input password
        :param hashed_password: hash's password from db
        :return: bool value
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)