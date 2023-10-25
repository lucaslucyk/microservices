import base64 as b64

# import jwt
from jose import JWTError, jwt
# from uuid import uuid1
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from schemas.tokens import TokenPayload
from auth.models.users import User as UserModel
from auth.crud.user import users


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


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[UserModel]:
    user = await users.find_one(db=db, email=email)
    if not user:
        return

    if not PasswordHasher.verify(password, user.hashed_password):
        return

    return user


def create_access_token(payload: TokenPayload) -> str:
    """Create an access token for a specific sub

    Args:
        sub (Union[str, int, Any]): User, session or other

    Returns:
        str: JWT Token
    """
    created = datetime.utcnow()
    payload.iat = int(created.timestamp())
    payload.exp = int(
        (created + timedelta(minutes=settings.TOKEN_EXPIRE_MINS)).timestamp()
    )

    # create token
    return jwt.encode(
        claims=payload.model_dump(mode="json", exclude_none=True),
        key=b64.b64decode(settings.PRIVATE_KEY),
        algorithm=settings.TOKEN_ALGORITHM,
    )
