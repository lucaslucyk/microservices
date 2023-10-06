from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from auth_pkg.schemas.tokens import Token, TokenPayload
from auth_pkg.crud.user import users

from core.config import settings
from core.security import PasswordHasher, create_access_token
from dependencies import get_db


router = APIRouter(include_in_schema=True)


@router.post("/login", response_model=Token)
async def login_access_token(
    *,
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    usr = await users.find_one(db=db, email=form_data.username)
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not PasswordHasher.verify(
        plain_password=form_data.password, hashed_password=usr.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        )

    if not usr.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )

    # get time offset
    # token_exp = timedelta(minutes=settings.TOKEN_EXPIRE_MINS)
    return Token(
        access_token=create_access_token(sub=str(usr.id), uuid=str(usr.uuid)),
        token_type="Bearer",
        expires_in=settings.TOKEN_EXPIRE_MINS,
    )
