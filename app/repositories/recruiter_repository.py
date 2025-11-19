from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import Offer, OfferTemplate, Recruiter, User


class RecruiterRepository:
    """Data access helper for recruiters and their related offer data."""

    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return (
            self.db.query(Recruiter)
            .options(
                selectinload(Recruiter.user),
                selectinload(Recruiter.offer_templates),
                selectinload(Recruiter.offers),
            )
        )

    def list(self) -> list[Recruiter]:
        return self._query().all()

    def get(self, recruiter_id: UUID) -> Recruiter | None:
        return self._query().filter(Recruiter.id == recruiter_id).first()

    def list_offer_templates(self, recruiter_id: UUID) -> list[OfferTemplate]:
        return (
            self.db.query(OfferTemplate)
            .filter(OfferTemplate.recruiter_id == recruiter_id)
            .all()
        )

    def list_offers(self, recruiter_id: UUID) -> list[Offer]:
        return (
            self.db.query(Offer)
            .filter(Offer.recruiter_id == recruiter_id)
            .all()
        )
