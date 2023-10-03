import logging
from typing import List
from uuid import uuid1
from fastapi import FastAPI, Path, status
from auth_pkg.schemas.public import UserCreate, UserUpdate, User
from auth_pkg.schemas.admin import UserKind, UserInDB


FAKE_DB: List[User] = []


app = FastAPI()


@app.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user_register(data: UserCreate) -> User:
    usr = UserInDB(
        email=data.email,
        kind=UserKind.patient,
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
@app.get('/{id}', response_model=User)
async def get_user(id: int = Path(...)) -> User:
    return FAKE_DB[id]


# TODO: convert to / endpoint with auth
@app.patch('/{id}', response_model=User)
async def update_user(
    *,
    id: int = Path(...),
    data: UserUpdate
) -> User:
    FAKE_DB[id].hashed_password=f'{data.password}--fake-hashed'
    return FAKE_DB[id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        # reload=True,
        # log_level="debug"
        # host='0.0.0.0',
        # port=8000,
        # log_level='warning'
        # reload_dirs=[os.path.join(os.path.dirname(__file__), 'app')]
    )