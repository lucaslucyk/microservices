from typing import Any, Iterable, Type, TypeVar
from uuid import UUID
from pydantic import TypeAdapter, BaseModel
from db.session import AsyncSessionLocal
from auth.crud.user import users as crud_users
from core.security import PasswordHasher
from auth.schemas.admin import UserCreate, UserCreateDB
from auth.models.users import User as UserModel


KindType = TypeVar("KindType", bound=BaseModel)


def parse_object_as(kind: Type[KindType], data: Any, **kwargs) -> KindType:
    """Parse python object to pydantic model type

    Args:
        kind (Any): Pydantic model type
        data (Any): Python object

    Returns:
        Any: Pydantic model type instance
    """

    return TypeAdapter(kind).validate_python(data, **kwargs)


async def create_user(user: UserCreate) -> UserModel:
    async with AsyncSessionLocal() as db:
        ucdb = UserCreateDB(
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            hashed_password=PasswordHasher.hash(user.password),
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
    

