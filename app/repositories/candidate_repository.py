from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import Candidate, JobPreferences, JobPreferencesSector


class CandidateRepository:
    """Data access helpers for candidate entities."""

    def __init__(self, db: Session):
        """Store SQLAlchemy session for future queries."""
        self.db = db

    def _query_with_relationships(self):
        """Base query including the relationships needed by services."""
        return self.db.query(Candidate).options(
            selectinload(Candidate.skills),
            selectinload(Candidate.languages),
            selectinload(Candidate.educations),
            selectinload(Candidate.experiences),
            selectinload(Candidate.job_preferences),
            selectinload(Candidate.applications),
            selectinload(Candidate.saved_job_offers),
        )

    def list(self) -> list[Candidate]:
        """Return all candidates with their relationships eagerly loaded."""
        return self._query_with_relationships().all()

    def get(self, candidate_id: UUID) -> Candidate | None:
        """Retrieve a candidate by identifier."""
        return (
            self._query_with_relationships()
            .filter(Candidate.id == candidate_id)
            .first()
        )
    
    def get_by_user_id(self, user_id: UUID) -> Candidate | None:
        """Retrieve the candidate linked to the provided user id."""
        return (
            self._query_with_relationships()
            .filter(Candidate.user_id == user_id)
            .first()
        )
