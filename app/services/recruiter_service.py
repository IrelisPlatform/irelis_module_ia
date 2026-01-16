from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.recruiter_repository import RecruiterRepository
from app.schemas import RecruiterRead
from app.utils.cache import APP_CACHE, make_cache_key


class RecruiterService:
    """Orchestrates recruiter data access."""

    def __init__(self, db: Session):
        """Inject dependencies."""
        self.repo = RecruiterRepository(db)

    def list_recruiters(self) -> list[RecruiterRead]:
        """Return every recruiter profile mapped to schema."""
        cache_key = make_cache_key("recruiters:list")
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached
        recruiters = [RecruiterRead.model_validate(rec) for rec in self.repo.list()]
        APP_CACHE.set(cache_key, recruiters)
        return recruiters

    def get_recruiter(self, recruiter_id: UUID) -> RecruiterRead | None:
        """Retrieve a single recruiter by identifier."""
        cache_key = make_cache_key("recruiters:get", recruiter_id)
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached
        recruiter = self.repo.get(recruiter_id)
        recruiter_read = RecruiterRead.model_validate(recruiter) if recruiter else None
        APP_CACHE.set(cache_key, recruiter_read)
        return recruiter_read
