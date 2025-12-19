from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import CandidateRead
from app.services.candidate_service import CandidateService

router = APIRouter()


@router.get("", response_model=list[CandidateRead], tags=["candidats"])
def list_candidates(
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[CandidateRead]:
    """Return every candidate profile."""
    return CandidateService(db).list_candidates()


# @router.get(
#     "/{candidate_id}",
#     response_model=CandidateRead,
#     tags=["candidats"],
# )
def get_candidate(
    candidate_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> CandidateRead:
    """Fetch a single candidate by identifier."""
    candidate = CandidateService(db).get_candidate(candidate_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate

# @router.get(
#     "/by_user/{user_id}",
#     response_model=CandidateRead,
#     tags=["candidats"],
# )
def get_candidate_by_user(
    user_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> CandidateRead:
    """Retrieve the candidate entity bound to a specific user account."""
    candidate = CandidateService(db).get_candidate_by_user(user_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate
