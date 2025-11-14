from sqlalchemy.orm import Session

from app.core.logging import logger
from app.db import base  # noqa: F401 imported for side-effects
from app.db.base import Base
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import UserService


def init_db(db: Session) -> None:
    logger.info("Initializing database")
    bind = db.get_bind()
    Base.metadata.create_all(bind=bind)

    service = UserService(db)
    admin_email = "admin@irelis.local"
    if service.get_by_email(admin_email):
        return

    service.create_user(
        UserCreate(
            email=admin_email,
            full_name="Admin",
            password="admin",
            is_active=True,
        )
    )
    logger.info("Default admin user created")
