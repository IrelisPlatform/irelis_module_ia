from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import JobOffer, Recruiter, User


class RecruiterRepository:
    """Data access helper for recruiters and their related offer data."""

    def __init__(self, db: Session):
        """Store SQLAlchemy session for reuse."""
        self.db = db

    def _query(self):
        """Return base query with data needed by services."""
        return (
            self.db.query(Recruiter)
            .options(
                selectinload(Recruiter.user),
                selectinload(Recruiter.sector),
                selectinload(Recruiter.job_offers),
            )
        )

    def list(self) -> list[Recruiter]:
        """Return every recruiter with user, sector, and offers preloaded."""
        return self._query().all()

    def get(self, recruiter_id: UUID) -> Recruiter | None:
        """Retrieve a recruiter by identifier."""
        return self._query().filter(Recruiter.id == recruiter_id).first()

    def get_by_user_id(self, user_id: UUID) -> Recruiter | None:
        """Fetch the recruiter profile bound to the given user."""
        return self._query().filter(Recruiter.user_id == user_id).first()

    def list_offers(self, recruiter_id: UUID) -> list[JobOffer]:
        """Return all offers owned by a recruiter."""
        return (
            self.db.query(JobOffer)
            .filter(JobOffer.company_id == recruiter_id)
            .all()
        )
