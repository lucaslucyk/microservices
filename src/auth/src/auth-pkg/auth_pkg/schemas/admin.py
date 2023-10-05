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
    # uuid: UUID1 = Field(default_factory=uuid1)

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: Optional[int] = None
    uuid: UUID1 = Field(default_factory=uuid1)
    token: str
    is_active: bool
    is_superuser: bool
    hashed_password: str
    # created_at: datetime = Field(default_factory=datetime.now)
    # updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class User(UserInDB):
    ...


class UserActivate(BaseModel):
    uuid: UUID1
    token: str