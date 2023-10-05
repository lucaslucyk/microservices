from typing import List
from uuid import uuid1
from fastapi import APIRouter, Path, status
from auth_pkg.schemas.public import UserCreate, UserUpdate, User
from auth_pkg.schemas.admin import UserInDB


FAKE_DB: List[User] = []


router = APIRouter()


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user_register(data: UserCreate) -> User:
    usr = UserInDB(
        email=data.email,
        id=len(FAKE_DB),
        uuid=uuid1(),
        token='fake-token',
        is_active=False,
        is_superuser=False,
        hashed_password=f'{data.password}--fake-hashed'
    )
    FAKE_DB.append(usr)
    return usr

# TODO: convert to / endpoint with auth
@router.get('/{id}', response_model=User)
async def get_user(id: int = Path(...)) -> User:
    return FAKE_DB[id]


# TODO: convert to / endpoint with auth
@router.patch('/{id}', response_model=User)
async def update_user(
    *,
    id: int = Path(...),
    data: UserUpdate
) -> User:
    FAKE_DB[id].hashed_password=f'{data.password}--fake-hashed'
    return FAKE_DB[id]
