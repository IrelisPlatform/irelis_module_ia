from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import OfferRead, OfferTemplateRead, RecruiterRead
from app.services.offer_service import OfferService
from app.services.offer_template_service import OfferTemplateService
from app.services.recruiter_service import RecruiterService

router = APIRouter()


@router.get("/recruiters", response_model=list[RecruiterRead], tags=["recruiters"])
def list_recruiters(db: Annotated[Session, Depends(deps.get_db)]) -> list[RecruiterRead]:
    return RecruiterService(db).list_recruiters()


@router.get(
    "/recruiters/{recruiter_id}",
    response_model=RecruiterRead,
    tags=["recruiters"],
)
def get_recruiter(
    recruiter_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> RecruiterRead:
    recruiter = RecruiterService(db).get_recruiter(recruiter_id)
    if recruiter is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruiter not found")
    return recruiter


@router.get(
    "/recruiters/{recruiter_id}/modeles_offres",
    response_model=list[OfferTemplateRead],
    tags=["recruiters", "modeles_offres"],
)
def list_templates_for_recruiter(
    recruiter_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[OfferTemplateRead]:
    return OfferTemplateService(db).list_by_recruiter(recruiter_id)


@router.get(
    "/recruiters/{recruiter_id}/offres",
    response_model=list[OfferRead],
    tags=["recruiters", "offres"],
)
def list_offers_for_recruiter(
    recruiter_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[OfferRead]:
    return OfferService(db).list_by_recruiter(recruiter_id)
