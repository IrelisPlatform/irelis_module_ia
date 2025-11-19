from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import Offer


class OfferRepository:
    """Data access helper for concrete offers."""

    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return self.db.query(Offer).options(
            selectinload(Offer.skills),
            selectinload(Offer.recruiter),
        )

    def list(self) -> list[Offer]:
        return self._query().all()

    def get(self, offer_id: UUID) -> Offer | None:
        return self._query().filter(Offer.id == offer_id).first()

    def list_by_recruiter(self, recruiter_id: UUID) -> list[Offer]:
        return (
            self._query()
            .filter(Offer.recruiter_id == recruiter_id)
            .all()
        )
