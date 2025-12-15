from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import Candidate, User


class UserRepository:
    """Minimal data access helpers for user entities."""

    def __init__(self, db: Session):
        """Store SQLAlchemy session for reuse."""
        self.db = db

    def _query(self):
        """Return base query for users with joined candidate relationships."""
        return (
            self.db.query(User)
            .options(
                selectinload(User.candidate)
                .selectinload(Candidate.skills),
                selectinload(User.candidate)
                .selectinload(Candidate.languages),
                selectinload(User.candidate)
                .selectinload(Candidate.educations),
                selectinload(User.candidate)
                .selectinload(Candidate.experiences),
                selectinload(User.candidate)
                .selectinload(Candidate.job_preferences),
            )
        )

    def get_candidate_by_user_id(self, user_id: UUID) -> Candidate | None:
        """Return the candidate tied to the provided user id."""
        user = self._query().filter(User.id == user_id).first()
        if user is None:
            return None
        return user.candidate
    
    def get(self, user_id: UUID) -> User | None:
        """Fetch a raw user entity by identifier."""
        return self.db.query(User).filter(User.id == user_id).first()
