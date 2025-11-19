from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so their metadata is registered on Base  # noqa: E402
from app import models  # noqa: F401
