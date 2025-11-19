from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import OfferTemplateRead
from app.services.offer_template_service import OfferTemplateService

router = APIRouter()


@router.get("/modeles_offres", response_model=list[OfferTemplateRead], tags=["modeles_offres"])
def list_offer_templates(
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[OfferTemplateRead]:
    return OfferTemplateService(db).list_templates()


@router.get(
    "/modeles_offres/{template_id}",
    response_model=OfferTemplateRead,
    tags=["modeles_offres"],
)
def get_offer_template(
    template_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> OfferTemplateRead:
    template = OfferTemplateService(db).get_template(template_id)
    if template is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modèle d'offre introuvable")
    return template
