# import jwt
from jose import jwt, JWTError
import base64 as b64
from typing import Any, Generator
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import async_session
from core.config import settings
from schemas.tokens import TokenPayload


# auth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


async def get_db() -> Generator[AsyncSession, Any, None]:
    """Get Async db session generator with aiosqlite engine.

    Yields:
        Generator: Async session generated with async engine and AsyncSession
    """
    async with async_session() as db_session:
        yield db_session


async def get_token_data(
    *, token: str = Security(oauth2_scheme)
) -> TokenPayload:
    """Get token payload from token header

    Args:
        token (str, optional):
            Bearer Token string. Defaults to Security(oauth2_scheme).

    Raises:
        HTTPException: HTTP 400/1 if something was wrong

    Returns:
        TokenPayload: Token payload data
    """

    try:
        payload = jwt.decode(
            token,
            b64.b64decode(settings.PUBLIC_KEY),
            algorithms=[settings.TOKEN_ALGORITHM],
        )
        return TokenPayload(**payload)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something was wrong",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_superuser_token(
    *, token_data: TokenPayload = Depends(get_token_data)
) -> TokenPayload:
    if token_data.rol != "superuser":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something was wrong",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data