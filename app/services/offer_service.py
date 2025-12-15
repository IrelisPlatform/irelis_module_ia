from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.offer_repository import OfferRepository
from app.schemas import JobOfferRead


class OfferService:
    def __init__(self, db: Session):
        """Inject the SQLAlchemy session and wire repositories."""
        self.repo = OfferRepository(db)

    def list_offers(self) -> list[JobOfferRead]:
        """Return every offer mapped to pydantic schema."""
        return [JobOfferRead.model_validate(offer) for offer in self.repo.list()]

    def get_offer(self, offer_id: UUID) -> JobOfferRead | None:
        """Retrieve a single offer by identifier."""
        offer = self.repo.get(offer_id)
        if offer is None:
            return None
        return JobOfferRead.model_validate(offer)

    def list_by_recruiter(self, recruiter_id: UUID) -> list[JobOfferRead]:
        """List all offers belonging to a given recruiter."""
        offers = self.repo.list_by_recruiter(recruiter_id)
        return [JobOfferRead.model_validate(offer) for offer in offers]
