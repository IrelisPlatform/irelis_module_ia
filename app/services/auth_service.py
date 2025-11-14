from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.repositories.user_repo import UserRepository
from app.schemas.user import Token


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def authenticate(self, email: str, password: str) -> Token | None:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None

        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(subject=str(user.id), expires_delta=expires_delta)
        expires_at = datetime.utcnow() + expires_delta
        return Token(access_token=access_token, expires_at=expires_at)
