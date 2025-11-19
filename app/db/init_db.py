import logging
from sqlalchemy.orm import Session

from app.db import base  # noqa: F401 imported for side-effects
from app.db.base import Base

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    logger.info("Initializing database")
    bind = db.get_bind()
    Base.metadata.create_all(bind=bind)
    logger.info("Default admin user created")
