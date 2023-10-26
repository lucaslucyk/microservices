import base64 as b64
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models.users import User as UserModel
from auth.crud.user import users
from auth.core.security import PasswordHasher
from api.core.config import settings
from api.schemas.tokens import TokenPayload


password_hasher = PasswordHasher(schemas=settings.CRYPT_SCHEMAS)


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[UserModel]:
    user = await users.find_one(db=db, email=email)
    if not user:
        return

    if not password_hasher.verify(password, user.hashed_password):
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
