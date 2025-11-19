from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.search_repository import SearchRepository
from app.schemas import SearchRead


class SearchService:
    def __init__(self, db: Session):
        self.repo = SearchRepository(db)

    def list_searches(self) -> list[SearchRead]:
        return [SearchRead.model_validate(s) for s in self.repo.list()]

    def get_search(self, search_id: UUID) -> SearchRead | None:
        search = self.repo.get(search_id)
        if search is None:
            return None
        return SearchRead.model_validate(search)

    def list_by_user(self, user_id: UUID) -> list[SearchRead]:
        return [
            SearchRead.model_validate(s)
            for s in self.repo.list_by_user(user_id)
        ]
