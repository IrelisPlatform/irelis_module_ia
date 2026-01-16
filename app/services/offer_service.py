from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.offer_repository import OfferRepository
from app.schemas import JobOfferDto
from app.services.dto_mappers import offer_to_dto
from app.utils.cache import APP_CACHE, make_cache_key


class OfferService:
    def __init__(self, db: Session):
        """Inject the SQLAlchemy session and wire repositories."""
        self.repo = OfferRepository(db)

    def list_offers(self) -> list[JobOfferDto]:
        """Return every offer mapped to pydantic schema."""
        cache_key = make_cache_key("offers:list")
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached
        offers = [offer_to_dto(offer) for offer in self.repo.list()]
        APP_CACHE.set(cache_key, offers)
        return offers

    def get_offer(self, offer_id: UUID) -> JobOfferDto | None:
        """Retrieve a single offer by identifier."""
        cache_key = make_cache_key("offers:get", offer_id)
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached
        offer = self.repo.get(offer_id)
        offer_dto = offer_to_dto(offer) if offer else None
        APP_CACHE.set(cache_key, offer_dto)
        return offer_dto

    def list_by_recruiter(self, recruiter_id: UUID) -> list[JobOfferDto]:
        """List all offers belonging to a given recruiter."""
        cache_key = make_cache_key("offers:list_by_recruiter", recruiter_id)
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached
        offers = [offer_to_dto(offer) for offer in self.repo.list_by_recruiter(recruiter_id)]
        APP_CACHE.set(cache_key, offers)
        return offers
