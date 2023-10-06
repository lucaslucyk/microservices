from datetime import datetime
from typing import Optional
from uuid import uuid1
from pydantic import UUID1, BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserCreateBase(UserBase):
    email: EmailStr
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)


class UserCreate(UserCreateBase):
    password: str


class UserCreateDB(UserBase):
    hashed_password: str
    # token: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserUpdateDB(UserBase):
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    uuid: UUID1
    token: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserInDBBase):
    hashed_password: str

class User(UserInDBBase):
    ...


class UserActivate(BaseModel):
    uuid: UUID1
    token: str