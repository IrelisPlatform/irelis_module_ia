from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import MatchingScoreRequest, MatchingScoreResponse
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
    service = MatchingService(db)
    result = service.score_candidate_for_offer(payload.candidate_id, payload.offer_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidat ou offre introuvable",
        )
    return result
