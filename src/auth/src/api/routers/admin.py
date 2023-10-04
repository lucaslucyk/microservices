from typing import List
from fastapi import APIRouter
from uuid import uuid1
from fastapi import Path, status
from auth_pkg.schemas.admin import UserCreate, UserUpdate, User, UserKind, UserInDB
from core.config import settings

FAKE_DB: List[User] = []
router = APIRouter(include_in_schema=True)


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user_create(data: UserCreate) -> User:
    usr = UserInDB(
        email=data.email,
        kind=data.kind,
        id=len(FAKE_DB),
        uuid=uuid1(),
        token='fake-token',
        is_active=data.is_active,
        is_superuser=data.is_superuser,
        hashed_password=f'{data.password}--fake-hashed'
    )
    FAKE_DB.append(usr)
    return usr


@router.get('/{id}')
# @router.get('/{id}', response_model=User)
# async def get_user(id: int = Path(...)) -> User:
async def get_user(id: int = Path(...)):
    return {"db_name": settings.DB_NAME}
    print(FAKE_DB[id])
    return FAKE_DB[id]


@router.patch('/{id}', response_model=User)
async def update_user(
    *,
    id: int = Path(...),
    data: UserUpdate
) -> User:
    if data.email != None:
        FAKE_DB[id].email=data.email
    
    if data.password != None:
        FAKE_DB[id].hashed_password=f'{data.password}--fake-hashed'

    if data.kind != None:
        FAKE_DB[id].kind = data.kind
    if data.is_active != None:
        FAKE_DB[id].is_superuser = data.is_superuser
    if data.is_superuser != None:
        FAKE_DB[id].is_active = data.is_active

    return FAKE_DB[id]