from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.search_repository import SearchRepository
from app.repositories.user_repository import UserRepository
from app.schemas import JobOfferDto, SearchCreate
from app.services.dto_mappers import offer_to_dto
from app.utils.cache import APP_CACHE, make_cache_key


class SearchService:
    """Business logic dedicated to search workflows."""

    def __init__(self, db: Session):
        """Initialize repositories used for search workflows."""
        self.repo = SearchRepository(db)
        self.user_repo = UserRepository(db)

    def search_by_payload(self, payload: SearchCreate) -> list[JobOfferDto]:
        """Search offers with explicit payload filters."""
        cache_key = make_cache_key("search:payload", payload)
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached
        offers = [offer_to_dto(offer) for offer in self.repo.search_by_payload(payload)]
        APP_CACHE.set(cache_key, offers)
        return offers


    def search_for_candidate_by_user(
        self,
        user_id: UUID,
        payload: SearchCreate | None = None,
    ) -> list[JobOfferDto] | None:
        """Search offers for a given user, enriching filters with candidate data."""
        candidate = self.user_repo.get_candidate_by_user_id(user_id)
        
        if candidate is None:
            user = self.user_repo.get(user_id)
            if user is None: 
                return None
            else:
                cache_key = make_cache_key("search:by_user", user_id, payload=payload)
                found, cached = APP_CACHE.get(cache_key)
                if found:
                    self.repo.record_search(user_id, payload)
                    return cached
                offers = [offer_to_dto(offer) for offer in self.repo.search_by_payload(payload)]
                self.repo.record_search(user_id, payload)
                APP_CACHE.set(cache_key, offers)
                return offers

        filters = payload.model_dump(exclude_none=True) if payload else None
        cache_key = make_cache_key("search:by_candidate", user_id, filters=filters)
        found, cached = APP_CACHE.get(cache_key)
        if found:
            self.repo.record_search(user_id, payload)
            return cached
        offers = [offer_to_dto(offer) for offer in self.repo.search_for_candidate(candidate, filters)]
        self.repo.record_search(user_id, payload)
        APP_CACHE.set(cache_key, offers)
        return offers
