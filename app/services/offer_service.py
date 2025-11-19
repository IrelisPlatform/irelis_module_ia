from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.offer_repository import OfferRepository
from app.schemas import OfferRead


class OfferService:
    def __init__(self, db: Session):
        self.repo = OfferRepository(db)

    def list_offers(self) -> list[OfferRead]:
        return [OfferRead.model_validate(offer) for offer in self.repo.list()]

    def get_offer(self, offer_id: UUID) -> OfferRead | None:
        offer = self.repo.get(offer_id)
        if offer is None:
            return None
        return OfferRead.model_validate(offer)

    def list_by_recruiter(self, recruiter_id: UUID) -> list[OfferRead]:
        offers = self.repo.list_by_recruiter(recruiter_id)
        return [OfferRead.model_validate(offer) for offer in offers]
