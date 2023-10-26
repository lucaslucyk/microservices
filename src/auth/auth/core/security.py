from typing import List
from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self, schemas: List[str], deprecated: str = "auto") -> None:
        self._schemas = schemas
        self._deprecated = deprecated
        self._context = CryptContext(self._schemas, deprecated=self._deprecated)

    def hash(self, password: str) -> str:
        """Hash a plain str password

        Args:
            password (str): Plain password

        Returns:
            str: Hassed password
        """

        return self._context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify secret against an existing hash.

        Args:
            plain_password (str): Password to verify
            hashed_password (str): Hashed password

        Returns:
            bool: `True` if the password matched the hash, else `False`.
        """

        try:
            return self._context.verify(plain_password, hashed_password)
        except ValueError:
            return False
