from datetime import datetime
from typing import Optional
from pydantic import UUID1, BaseModel, EmailStr, Field, field_validator
from ..utils.validators import password_validator


class UserBase(BaseModel):
    email: EmailStr


class UserPassword(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def pwd_validator(cls, value: str):
        return password_validator(value=value)


class UserFields(BaseModel):
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)


class UserCreate(UserBase, UserFields, UserPassword):
    ...


class UserCreateDB(UserBase, UserFields):
    hashed_password: str


class UserUpdate(UserBase, UserFields, UserPassword):
    email: Optional[EmailStr] = None
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)

    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def pwd_validator(cls, value: str):
        return password_validator(value=value)