from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.candidate_repository import CandidateRepository
from app.schemas import CandidateRead


class CandidateService:
    """Business logic for candidate resources."""

    def __init__(self, db: Session):
        """Wire repositories used by the service."""
        self.repo = CandidateRepository(db)

    def list_candidates(self) -> list[CandidateRead]:
        """Return all candidates mapped to read schemas."""
        candidates = self.repo.list()
        return [CandidateRead.model_validate(candidate) for candidate in candidates]

    def get_candidate(self, candidate_id: UUID) -> CandidateRead | None:
        """Retrieve a single candidate by identifier."""
        candidate = self.repo.get(candidate_id)
        if candidate is None:
            return None
        return CandidateRead.model_validate(candidate)
    
    def get_candidate_by_user(self, user_id: UUID) -> CandidateRead | None:
        """Return the candidate entity associated with a given user."""
        candidate = self.repo.get_by_user_id(user_id)
        if candidate is None:
            return None
        return CandidateRead.model_validate(candidate)
