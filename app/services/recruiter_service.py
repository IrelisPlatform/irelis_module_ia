from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.recruiter_repository import RecruiterRepository
from app.schemas import RecruiterRead


class RecruiterService:
    """Orchestrates recruiter data access."""

    def __init__(self, db: Session):
        """Inject dependencies."""
        self.repo = RecruiterRepository(db)

    def list_recruiters(self) -> list[RecruiterRead]:
        """Return every recruiter profile mapped to schema."""
        recruiters = self.repo.list()
        return [RecruiterRead.model_validate(rec) for rec in recruiters]

    def get_recruiter(self, recruiter_id: UUID) -> RecruiterRead | None:
        """Retrieve a single recruiter by identifier."""
        recruiter = self.repo.get(recruiter_id)
        if recruiter is None:
            return None
        return RecruiterRead.model_validate(recruiter)
