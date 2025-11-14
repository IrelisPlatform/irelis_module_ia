from datetime import datetime, timedelta

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: datetime | None = None

    @staticmethod
    def expiration_from_delta(delta: timedelta) -> datetime:
        return datetime.utcnow() + delta
