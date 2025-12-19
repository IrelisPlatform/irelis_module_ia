from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import SearchTarget, SearchType
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.recruiter_repository import RecruiterRepository
from app.repositories.search_repository import SearchRepository
from app.repositories.user_repository import UserRepository
from app.schemas import CandidateRead, SearchCreate


class CandidateService:
    """Business logic for candidate resources."""

    def __init__(self, db: Session):
        """Wire repositories used by the service."""
        self.repo = CandidateRepository(db)
        self.user_repo = UserRepository(db)
        self.recruiter_repo = RecruiterRepository(db)
        self.search_repo = SearchRepository(db)

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

    def search_by_boolean_query(self, query: str, user_id: UUID) -> list[CandidateRead]:
        """Execute a boolean search across candidate profiles."""
        user = self.user_repo.get(user_id)
        if user is None:
            raise LookupError("Utilisateur introuvable")

        recruiter = self.recruiter_repo.get_by_user_id(user_id)
        if recruiter is None:
            raise PermissionError(
                "L'utilisateur n'est associé à aucun compte recruteur"
            )

        candidates = self.repo.search_by_boolean_query(query)

        payload = SearchCreate(
            user_id=user_id,
            query=query,
            type=SearchType.BOOL,
            target=SearchTarget.CANDIDAT,
        )
        self.search_repo.record_search(user_id, payload)

        return [CandidateRead.model_validate(candidate) for candidate in candidates]
