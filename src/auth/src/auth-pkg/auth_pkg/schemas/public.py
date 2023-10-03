from pydantic import BaseModel, EmailStr, UUID1


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    password: str


class User(UserBase):
    id: int
    uuid: UUID1
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True