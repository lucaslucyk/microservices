from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth_db.exceptions.db import (
    CreateException,
    UserActivateException,
    NotFoundException,
)
from auth_db.schemas.admin import (
    UserCreate,
    UserUpdate,
    User,
    UserCreateDB,
    UserUpdateDB,
    UserActivate,
)
from auth_db.schemas.public import (
    User as PublicUser,
    UserUpdate as PublicUserUpdate
)
from auth_db.crud.user import users
from dependencies import get_db, get_token_data, get_superuser_token
from core.security import PasswordHasher
from schemas.tokens import TokenPayload


router = APIRouter(include_in_schema=True)


@router.get("/", response_model=List[User])
async def get_users(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_superuser_token)
) -> List[User]:
    return await users.list(db=db)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user_create(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_superuser_token),
    data: UserCreate
) -> User:
    try:
        usr = UserCreateDB(
            **data.model_dump(),
            hashed_password=PasswordHasher.hash(password=data.password),
        )
        return await users.create(db=db, data=usr)

    except CreateException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )


@router.get("/me/", response_model=PublicUser)
async def get_user(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_token_data)
) -> PublicUser:
    try:
        return await users.get_or_raise(db=db, uid=token_data.uid)

    except NotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        )


@router.patch("/me/", response_model=PublicUser)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_token_data),
    data: PublicUserUpdate
) -> PublicUser:
    try:
        db_user = await users.get_or_raise(db=db, uid=token_data.uid)
        db_upd = UserUpdateDB(
            hashed_password=PasswordHasher.hash(password=data.password)
        )
        return await users.update(db=db, obj=db_user, data=db_upd)

    except NotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        )


@router.delete("/me/", response_model=User)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_token_data)
) -> User:
    try:
        # TODO: Send current token to blacklist
        return await users.delete(db=db, uid=token_data.uid)

    except NotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        )
    

@router.get("/{uid}/", response_model=User)
async def get_user(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_superuser_token),
    uid: UUID = Path(...)
) -> User:
    try:
        return await users.get_or_raise(db=db, uid=uid)

    except NotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        )


@router.patch("/{uid}/", response_model=User)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_superuser_token),
    uid: UUID = Path(...),
    data: UserUpdate
) -> User:
    try:
        db_user = await users.get_or_raise(db=db, uid=uid)
        db_upd = UserUpdateDB(**data.model_dump(exclude_unset=True))
        if data.password != None:
            db_upd.hashed_password = PasswordHasher.hash(password=data.password)
        return await users.update(db=db, obj=db_user, data=db_upd)

    except NotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        )


@router.delete("/{uid}/", response_model=User)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_superuser_token),
    uid: UUID = Path(...)
) -> User:
    try:
        return await users.delete(db=db, uid=uid)

    except NotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        )


@router.post("/activate/", response_model=PublicUser)
async def activate_user(
    *, db: AsyncSession = Depends(get_db), data: UserActivate
) -> PublicUser:
    try:
        return await users.activate(db=db, data=data)
    except UserActivateException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )
