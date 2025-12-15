from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import JobOffer


class OfferRepository:
    """Data access helper for concrete offers."""

    def __init__(self, db: Session):
        """Store session for reuse."""
        self.db = db

    def _query(self):
        """Base query selecting the relationships required by services."""
        return self.db.query(JobOffer).options(
            selectinload(JobOffer.recruiter),
            selectinload(JobOffer.applications),
            selectinload(JobOffer.tags),
            selectinload(JobOffer.required_documents),
            selectinload(JobOffer.candidature_info),
        )

    def list(self) -> list[JobOffer]:
        """Return every offer with eager-loaded relationships."""
        return self._query().all()

    def get(self, offer_id: UUID) -> JobOffer | None:
        """Retrieve a single offer by identifier."""
        return self._query().filter(JobOffer.id == offer_id).first()

    def list_by_recruiter(self, recruiter_id: UUID) -> list[JobOffer]:
        """Return all offers created by a recruiter."""
        return (
            self._query()
            .filter(JobOffer.company_id == recruiter_id)
            .all()
        )
