from typing import Optional
from uuid import UUID, uuid1
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenPayload(BaseModel):
    # iss: Optional[str] = None
    sub: Optional[str] = None
    rol: Optional[str] = None
    uuid: Optional[UUID] = None
    email: Optional[str] = None
    # aud: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    jti: Optional[UUID] = Field(default_factory=uuid1)