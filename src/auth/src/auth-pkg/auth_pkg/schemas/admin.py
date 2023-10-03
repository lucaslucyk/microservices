from enum import Enum
from typing import Optional
from uuid import uuid1
from pydantic import UUID1, BaseModel, EmailStr, Field


class UserKind(Enum):
    patient = 0
    doctor = 1
    staff = 2


class UserBase(BaseModel):
    email: EmailStr
    kind: Optional[UserKind] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserCreateBase(UserBase):
    email: EmailStr
    kind: UserKind = Field(default=UserKind.patient)
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)


class UserCreate(UserCreateBase):
    password: str


class UserCreateDB(UserBase):
    hashed_password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    uuid: UUID1 = Field(default_factory=uuid1)
    token: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    ...


class UserActivate(BaseModel):
    uuid: UUID1
    token: str