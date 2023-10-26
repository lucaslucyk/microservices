from typing import Iterable
from uuid import UUID
from auth.crud.user import users as crud_users
from auth.core.security import PasswordHasher
from auth.schemas.admin import UserCreate, UserCreateDB
from auth.models.users import User as UserModel
from cli.config import settings
from cli.session import AsyncSessionLocal


async def create_user(user: UserCreate) -> UserModel:
    password_hasher = PasswordHasher(schemas=settings.CRYPT_SCHEMAS)
    async with AsyncSessionLocal() as db:
        ucdb = UserCreateDB(
            **user.model_dump(),
            hashed_password=password_hasher.hash(password=user.password),
        )
        return await crud_users.create(db=db, element=ucdb)


async def delete_user(uid: UUID) -> UserModel:
    async with AsyncSessionLocal() as db:
        return await crud_users.delete(db=db, uid=uid)


async def list_users(offset: int = 0, limit: int = 100) -> Iterable[UserModel]:
    async with AsyncSessionLocal() as db:
        return await crud_users.list(db=db, offset=offset, limit=limit)


async def get_user(uid: UUID) -> Iterable[UserModel]:
    async with AsyncSessionLocal() as db:
        return await crud_users.get_or_raise(db=db, uid=uid)
