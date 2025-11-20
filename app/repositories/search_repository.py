from __future__ import annotations      


from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Search


class SearchRepository:
    """Data access for search records."""

    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Search]:
        return self.db.query(Search).all()

    def get(self, search_id: UUID) -> Search | None:
        return (
            self.db.query(Search)
            .filter(Search.id == search_id)
            .first()
        )

    def list_by_user(self, user_id: UUID) -> list[Search]:
        return (
            self.db.query(Search)
            .filter(Search.user_id == user_id)
            .all()
        )
