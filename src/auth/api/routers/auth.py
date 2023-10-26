from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.tokens import Token, TokenPayload
from api.core.config import settings
from api.core.security import (
    create_access_token,
    authenticate_user,
    decode_access_token,
)
from api.dependencies import get_db


router = APIRouter(include_in_schema=True)


@router.post("/verify/", response_model=dict)
async def verify_access_token(*, token: Token = Body(...)) -> JSONResponse:
    try:
        decode_access_token(token=token.access_token)
        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )


@router.post("/login/", response_model=Token)
async def login_access_token(
    *,
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    usr = await authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usr.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(
        access_token=create_access_token(
            payload=TokenPayload(
                sub=str(usr.id),
                rol="superuser" if usr.is_superuser else "user",
                uid=usr.uid,
                email=usr.email,
            )
        ),
        token_type="Bearer",
        expires_in=settings.TOKEN_EXPIRE_MINS,
    )
