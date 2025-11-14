from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserRead


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def list_users(self) -> list[UserRead]:
        return [UserRead.model_validate(user) for user in self.repo.list()]

    def get_by_email(self, email: str) -> User | None:
        return self.repo.get_by_email(email)

    def create_user(self, payload: UserCreate) -> UserRead:
        if self.repo.get_by_email(payload.email):
            raise ValueError("User already exists")

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
            is_active=payload.is_active,
        )
        created = self.repo.create(user)
        return UserRead.model_validate(created)
