from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.offer_template_repository import OfferTemplateRepository
from app.schemas import OfferTemplateRead


class OfferTemplateService:
    def __init__(self, db: Session):
        self.repo = OfferTemplateRepository(db)

    def list_templates(self) -> list[OfferTemplateRead]:
        return [OfferTemplateRead.model_validate(tpl) for tpl in self.repo.list()]

    def get_template(self, template_id: UUID) -> OfferTemplateRead | None:
        template = self.repo.get(template_id)
        if template is None:
            return None
        return OfferTemplateRead.model_validate(template)

    def list_by_recruiter(self, recruiter_id: UUID) -> list[OfferTemplateRead]:
        templates = self.repo.list_by_recruiter(recruiter_id)
        return [OfferTemplateRead.model_validate(tpl) for tpl in templates]
