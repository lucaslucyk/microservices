import base64 as b64
import jwt
from uuid import uuid1
from datetime import datetime, timedelta
from typing import Union, Any

from core.config import settings
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from passlib.exc import UnknownHashError


crypt_context = CryptContext(settings.CRYPT_SCHEMAS, deprecated="auto")
cipher = Fernet(settings.SECRET_KEY)


class PasswordHasher:
    @staticmethod
    def verify(plain_password, hashed_password):
        try:
            return crypt_context.verify(plain_password, hashed_password)
        except ValueError:
            return False

    @staticmethod
    def hash(password):
        return crypt_context.hash(password)


class PasswordCipher:
    @staticmethod
    def encrypt(password: str) -> str:
        """Encrypt a password using Fernet cipher

        Args:
            password (str): Password to encrypt

        Returns:
            str: Crypted password
        """

        return cipher.encrypt(password.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decrypt(encrypted_password: str) -> str:
        """Decrypt a Fernet encrypted

        Args:
            encrypted_password (str): Encrypted password

        Returns:
            str: Decrypted password
        """
        enc = "utf-8"
        return cipher.decrypt(encrypted_password.encode(enc)).decode(enc)


def create_access_token(sub: Union[str, int, Any], uuid: str) -> str:
    """Create an access token for a specific sub

    Args:
        sub (Union[str, int, Any]): User, session or other

    Returns:
        str: JWT Token
    """

    # expire time
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINS)

    # base keys
    to_encode = {"uuid": uuid, "sub": str(sub), "exp": int(expire.timestamp())}

    # create token
    return jwt.encode(
        payload=to_encode,
        key=b64.b64decode(settings.PRIVATE_KEY),
        algorithm=settings.TOKEN_ALGORITHM,
    )
