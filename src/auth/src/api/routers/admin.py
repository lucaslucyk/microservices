from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth_pkg.exceptions.db import UserActivateException
from auth_pkg.schemas.admin import (
    UserCreate,
    UserUpdate,
    User,
    UserCreateDB,
    UserUpdateDB,
    UserActivate,
)
from auth_pkg.crud.user import users
from dependencies import get_db
from core.security import PasswordHasher


router = APIRouter(include_in_schema=True)


@router.get("/", response_model=List[User])
async def get_users(*, db: AsyncSession = Depends(get_db)) -> List[User]:
    return await users.list(db=db)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user_create(
    *, db: AsyncSession = Depends(get_db), data: UserCreate
) -> User:
    # usr = UserCreateDB(
    #     email=data.email,
    #     is_active=data.is_active,
    #     is_superuser=data.is_superuser,
    #     hashed_password=f"{data.password}--fake-hashed",
    # )
    usr = UserCreateDB(
        **data.model_dump(),
        hashed_password=PasswordHasher.hash(password=data.password),
    )
    return await users.create(db=db, data=usr)


@router.get("/{id}", response_model=User)
async def get_user(
    *, db: AsyncSession = Depends(get_db), id: int = Path(...)
) -> User:
    return await users.get_or_raise(db=db, id=id)


@router.patch("/{id}", response_model=User)
async def update_user(
    *, db: AsyncSession = Depends(get_db), id: int = Path(...), data: UserUpdate
) -> User:
    db_user = await users.get_or_raise(db=db, id=id)
    db_upd = UserUpdateDB(**data.model_dump(exclude_unset=True))
    if data.password != None:
        db_upd.hashed_password=PasswordHasher.hash(password=data.password)
    return await users.update(db=db, obj=db_user, data=db_upd)


@router.post("/activate", response_model=User)
async def activate_user(
    *, db: AsyncSession = Depends(get_db), data: UserActivate
) -> User:
    try:
        return await users.activate(db=db, data=data)
    except UserActivateException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )
