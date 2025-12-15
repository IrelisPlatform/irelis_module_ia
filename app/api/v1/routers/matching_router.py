from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import (
    CandidateRecommendationsResponse,
    MatchingScoreRequest,
    MatchingScoreResponse,
)
from app.services.matching_service import MatchingService


router = APIRouter()


@router.post(
    "/matching/score",
    response_model=MatchingScoreResponse,
    tags=["matching"],
)
def compute_matching_score(
    payload: MatchingScoreRequest,
    db: Annotated[Session, Depends(deps.get_db)],
) -> MatchingScoreResponse:
    """Compute a compatibility score between one candidate and one job offer."""
    service = MatchingService(db)
    result = service.score_candidate_for_offer(payload.candidate_id, payload.offer_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidat ou offre introuvable",
        )
    return result


@router.get(
    "/recommendations",
    response_model=CandidateRecommendationsResponse,
    tags=["matching"],
)
def get_recommendations(
    db: Annotated[Session, Depends(deps.get_db)],
    candidate_id: UUID = Query(..., alias="candidateId"),
    k: int = Query(10, ge=1, le=50),
) -> CandidateRecommendationsResponse:
    """Return the top-k offers ranked for the provided candidate."""
    service = MatchingService(db)
    response = service.recommend_offers_for_candidate(candidate_id, k)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidat introuvable",
        )

    return response
