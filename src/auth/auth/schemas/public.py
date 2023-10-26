from pydantic import BaseModel, EmailStr, UUID1, field_validator

from auth.models.users import UserKind
from ..utils.validators import password_validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def pwd_validator(cls, value: str):
        return password_validator(value=value)


class UserUpdate(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def pwd_validator(cls, value: str):
        return password_validator(value=value)


class User(UserBase):
    id: int
    uid: UUID1
    is_active: bool
    is_superuser: bool
    kind: UserKind

    class Config:
        from_attributes = True
