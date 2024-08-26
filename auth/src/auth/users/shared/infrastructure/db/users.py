from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from auth.users.shared.domain.users import User as UserDomain


class User(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        populate_defaults=True,
    )
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    password: Optional[str] = Field(default=None)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, value):
        if value is None:
            return value
        return str(value)

    def to_domain(self) -> UserDomain:
        return UserDomain(id=self.id, username=self.username)

    @staticmethod
    def from_domain(user: UserDomain) -> "User":
        return User(id=user.id, username=user.username)
