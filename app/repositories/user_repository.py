from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import Candidate, User


class UserRepository:
    """Minimal data access helpers for user entities."""

    def __init__(self, db: Session):
        self.db = db

    def get_candidate_by_user_id(self, user_id: UUID) -> Candidate | None:
        user = (
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
            .filter(User.id == user_id)
            .first()
        )
        if user is None:
            return None
        return user.candidate
