from typing import Optional
from uuid import UUID, uuid1
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: Optional[int] = None


class TokenPayload(BaseModel):
    # TODO: Add user kind field
    # iss: Optional[str] = None
    sub: Optional[str] = None
    rol: Optional[str] = None
    uid: Optional[UUID] = None
    email: Optional[str] = None
    # aud: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    jti: Optional[UUID] = Field(default_factory=uuid1)


class Jwk(BaseModel):
    kid: Optional[str] = None
    kty: Optional[str] = None
    alg: Optional[str] = None
    n: Optional[str] = None
    e: Optional[str] = None
    