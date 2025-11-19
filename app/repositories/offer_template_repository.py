from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models import OfferTemplate


class OfferTemplateRepository:
    """Data access helper for offer templates (Model offre)."""

    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return self.db.query(OfferTemplate).options(
            selectinload(OfferTemplate.skills)
        )

    def list(self) -> list[OfferTemplate]:
        return self._query().all()

    def get(self, template_id: UUID) -> OfferTemplate | None:
        return self._query().filter(OfferTemplate.id == template_id).first()

    def list_by_recruiter(self, recruiter_id: UUID) -> list[OfferTemplate]:
        return (
            self._query()
            .filter(OfferTemplate.recruiter_id == recruiter_id)
            .all()
        )
