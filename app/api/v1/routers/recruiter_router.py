from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import JobOfferDto, RecruiterRead
from app.services.offer_service import OfferService
from app.services.recruiter_service import RecruiterService
from app.utils.cache import APP_CACHE, make_cache_key

router = APIRouter()


@router.get("/recruiters", response_model=list[RecruiterRead], tags=["recruiters"])
def list_recruiters(db: Annotated[Session, Depends(deps.get_db)]) -> list[RecruiterRead]:
    """Return every recruiter profile with related metadata."""
    cache_key = make_cache_key("list_recruiters")
    cached = APP_CACHE.get(cache_key)
    if cached[0]:
        return cached[1]
    recruiters = RecruiterService(db).list_recruiters()
    APP_CACHE.set(cache_key, recruiters)
    return recruiters


@router.get(
    "/recruiters/{recruiter_id}",
    response_model=RecruiterRead,
    tags=["recruiters"],
)
def get_recruiter(
    recruiter_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> RecruiterRead:
    """Retrieve one recruiter by identifier."""
    cache_key = make_cache_key("get_recruiter", recruiter_id)
    cached = APP_CACHE.get(cache_key)
    if cached[0]:
        return cached[1]
    recruiter = RecruiterService(db).get_recruiter(recruiter_id)
    if recruiter is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruiter not found")
    APP_CACHE.set(cache_key, recruiter)
    return recruiter


@router.get(
    "/recruiters/{recruiter_id}/offres",
    response_model=list[JobOfferDto],
    tags=["recruiters", "offres"],
)
def list_offers_for_recruiter(
    recruiter_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[JobOfferDto]:
    """Return all job offers owned by a recruiter."""
    cache_key = make_cache_key("list_offers_for_recruiter", recruiter_id)
    cached = APP_CACHE.get(cache_key)
    if cached[0]:
        return cached[1]
    offers = OfferService(db).list_by_recruiter(recruiter_id)
    APP_CACHE.set(cache_key, offers)
    return offers
