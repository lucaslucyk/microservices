from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
# from auth_db.schemas.tokenss import Token, TokenPayload
from auth_db.crud.user import users

from schemas.tokens import Token, TokenPayload
from core.config import settings
from core.security import create_access_token, authenticate_user
from dependencies import get_db


router = APIRouter(include_in_schema=True)


@router.post("/login", response_model=Token)
async def login_access_token(
    *,
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    usr = await authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not usr.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return Token(
        access_token=create_access_token(payload=TokenPayload(
            sub=str(usr.id),
            rol="superuser" if usr.is_superuser else "user",
            uid=usr.uid,
            email=usr.email
        )),
        token_type="Bearer",
        expires_in=settings.TOKEN_EXPIRE_MINS,
    )
