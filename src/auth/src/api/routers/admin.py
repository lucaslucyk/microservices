from typing import List
from fastapi import APIRouter, Depends
from uuid import uuid1
from fastapi import Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from dependencies import get_db
from auth_pkg.schemas.admin import (
    UserCreate,
    UserUpdate,
    User,
    UserInDB,
    UserCreateDB
)
from auth_pkg.crud.user import users


FAKE_DB: List[User] = []
router = APIRouter(include_in_schema=True)


@router.get("/", response_model=List[User])
async def get_users(*, db: AsyncSession = Depends(get_db)) -> List[User]:
    return await users.list(db=db)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user_create(
    *, db: AsyncSession = Depends(get_db), data: UserCreate
) -> User:
    usr = UserCreateDB(
        email=data.email,
        # kind=data.kind,
        # uuid=uuid1(),
        # token="fake-token",
        is_active=data.is_active,
        is_superuser=data.is_superuser,
        hashed_password=f"{data.password}--fake-hashed",
    )
    return await users.create(db=db, data=usr)


@router.get("/{id}", response_model=User)
async def get_user(id: int = Path(...)) -> User:
    return FAKE_DB[id]


@router.patch("/{id}", response_model=User)
async def update_user(*, id: int = Path(...), data: UserUpdate) -> User:
    if data.email != None:
        FAKE_DB[id].email = data.email

    if data.password != None:
        FAKE_DB[id].hashed_password = f"{data.password}--fake-hashed"

    if data.kind != None:
        FAKE_DB[id].kind = data.kind
    if data.is_active != None:
        FAKE_DB[id].is_superuser = data.is_superuser
    if data.is_superuser != None:
        FAKE_DB[id].is_active = data.is_active

    return FAKE_DB[id]
