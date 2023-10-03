import logging
from typing import List
from uuid import uuid1
from fastapi import FastAPI, Path, status
from auth_pkg.schemas.admin import UserCreate, UserUpdate, User, UserKind, UserInDB


FAKE_DB: List[User] = []


app = FastAPI()


@app.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
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


@app.get('/{id}', response_model=User)
async def get_user(id: int = Path(...)) -> User:
    print(FAKE_DB[id])
    return FAKE_DB[id]


@app.patch('/{id}', response_model=User)
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        port=5000,
        # reload=True,
        # log_level="debug"
        # host='0.0.0.0',
        # log_level='warning'
        # reload_dirs=[os.path.join(os.path.dirname(__file__), 'app')]
    )