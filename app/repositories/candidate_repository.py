from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import Candidate


class CandidateRepository:
    """Data access helpers for candidate entities."""

    def __init__(self, db: Session):
        self.db = db

    def _query_with_relationships(self):
        return (
            self.db.query(Candidate)
            .options(
                selectinload(Candidate.skills),
                selectinload(Candidate.desired_positions),
                selectinload(Candidate.desired_position_types),
                selectinload(Candidate.educations),
                selectinload(Candidate.experiences),
                selectinload(Candidate.projects),
                selectinload(Candidate.languages),
            )
        )

    def list(self) -> list[Candidate]:
        return self._query_with_relationships().all()

    def get(self, candidate_id: UUID) -> Candidate | None:
        return (
            self._query_with_relationships()
            .filter(Candidate.id == candidate_id)
            .first()
        )
