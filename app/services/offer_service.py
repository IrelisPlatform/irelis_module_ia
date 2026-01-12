from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.offer_repository import OfferRepository
from app.schemas import JobOfferDto
from app.services.dto_mappers import offer_to_dto


class OfferService:
    def __init__(self, db: Session):
        """Inject the SQLAlchemy session and wire repositories."""
        self.repo = OfferRepository(db)

    def list_offers(self) -> list[JobOfferDto]:
        """Return every offer mapped to pydantic schema."""
        return [offer_to_dto(offer) for offer in self.repo.list()]

    def get_offer(self, offer_id: UUID) -> JobOfferDto | None:
        """Retrieve a single offer by identifier."""
        offer = self.repo.get(offer_id)
        if offer is None:
            return None
        return offer_to_dto(offer)

    def list_by_recruiter(self, recruiter_id: UUID) -> list[JobOfferDto]:
        """List all offers belonging to a given recruiter."""
        offers = self.repo.list_by_recruiter(recruiter_id)
        return [offer_to_dto(offer) for offer in offers]
