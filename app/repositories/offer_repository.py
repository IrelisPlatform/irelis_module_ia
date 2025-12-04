from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import JobOffer


class OfferRepository:
    """Data access helper for concrete offers."""

    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return self.db.query(JobOffer).options(
            selectinload(JobOffer.recruiter),
            selectinload(JobOffer.applications),
            selectinload(JobOffer.tags),
        )

    def list(self) -> list[JobOffer]:
        return self._query().all()

    def get(self, offer_id: UUID) -> JobOffer | None:
        return self._query().filter(JobOffer.id == offer_id).first()

    def list_by_recruiter(self, recruiter_id: UUID) -> list[JobOffer]:
        return (
            self._query()
            .filter(JobOffer.company_id == recruiter_id)
            .all()
        )
