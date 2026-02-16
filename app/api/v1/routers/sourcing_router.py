from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import SourcingSearchResponse
from app.services.matching_service import MatchingService
from app.utils.cache import APP_CACHE, make_cache_key


router = APIRouter()


@router.get(
    "/sourcing/search",
    response_model=SourcingSearchResponse,
    tags=["sourcing"],
)
def search_candidates_for_offer(
    db: Annotated[Session, Depends(deps.get_db)],
    offer_id: UUID = Query(..., alias="offerId"),
    limit: int = Query(10, ge=1, le=50),
) -> SourcingSearchResponse:
    """Rank candidates for a specific offer and return the best matches."""
    cache_key = make_cache_key("search_candidates_for_offer", offer_id, limit)
    cached = APP_CACHE.get(cache_key)
    if cached[0]:
        return cached[1]

    service = MatchingService(db)
    response = service.rank_candidates_for_offer(offer_id, limit)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre introuvable",
        )

    APP_CACHE.set(cache_key, response)
    return response
