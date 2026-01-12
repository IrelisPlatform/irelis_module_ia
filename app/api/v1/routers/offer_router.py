from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import JobOfferDto
from app.services.offer_service import OfferService

router = APIRouter()


@router.get("/offres", response_model=list[JobOfferDto], tags=["offres"])
def list_offers(db: Annotated[Session, Depends(deps.get_db)]) -> list[JobOfferDto]:
    """Return all job offers with their related data."""
    return OfferService(db).list_offers()


@router.get("/offres/{offer_id}", response_model=JobOfferDto, tags=["offres"])
def get_offer(
    offer_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> JobOfferDto:
    """Retrieve a single job offer by identifier."""
    offer = OfferService(db).get_offer(offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offre introuvable")
    return offer
