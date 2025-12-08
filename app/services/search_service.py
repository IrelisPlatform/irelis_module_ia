from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.search_repository import SearchRepository
from app.repositories.user_repository import UserRepository
from app.schemas import JobOfferRead, SearchCreate


class SearchService:
    """Business logic dedicated to search workflows."""

    def __init__(self, db: Session):
        self.repo = SearchRepository(db)
        self.user_repo = UserRepository(db)

    def search_by_payload(self, payload: SearchCreate) -> list[JobOfferRead]:
        offers = self.repo.search_by_payload(payload)
        return [JobOfferRead.model_validate(offer) for offer in offers]


    def search_for_candidate_by_user(
        self,
        user_id: UUID,
        payload: SearchCreate | None = None,
    ) -> list[JobOfferRead] | None:
        candidate = self.user_repo.get_candidate_by_user_id(user_id)
        if candidate is None:
            return None

        filters = payload.model_dump(exclude_none=True) if payload else None
        offers = self.repo.search_for_candidate(candidate, filters)
        self.repo.record_search(user_id, payload)
        return [JobOfferRead.model_validate(offer) for offer in offers]
