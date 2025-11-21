from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.candidate_repository import CandidateRepository
from app.schemas import CandidateRead


class CandidateService:
    """Business logic for candidate resources."""

    def __init__(self, db: Session):
        self.repo = CandidateRepository(db)

    def list_candidates(self) -> list[CandidateRead]:
        candidates = self.repo.list()
        return [CandidateRead.model_validate(candidate) for candidate in candidates]

    def get_candidate(self, candidate_id: UUID) -> CandidateRead | None:
        candidate = self.repo.get(candidate_id)
        if candidate is None:
            return None
        return CandidateRead.model_validate(candidate)
    
    def get_candidate_by_user(self, user_id: UUID) -> CandidateRead | None:
        candidate = self.repo.get_by_user_id(user_id)
        if candidate is None:
            return None
        return CandidateRead.model_validate(candidate)
