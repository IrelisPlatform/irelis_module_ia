from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import CandidateDto
from app.services.candidate_service import CandidateService

router = APIRouter()


@router.get("", response_model=list[CandidateDto], tags=["candidats"])
def list_candidates(
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[CandidateDto]:
    """Return every candidate profile."""
    return CandidateService(db).list_candidates()


@router.get(
    "/recherche/bool",
    response_model=list[CandidateDto],
    tags=["candidats"],
)
def boolean_search_candidates(
    db: Annotated[Session, Depends(deps.get_db)],
    user_id: UUID = Query(..., description="Identifiant du recruteur"),
    query: str = Query(..., min_length=1, description="Requête booléenne"),
) -> list[CandidateDto]:
    """Search candidates using boolean operators and nested expressions."""
    service = CandidateService(db)
    try:
        return service.search_by_boolean_query(query=query, user_id=user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


# @router.get(
#     "/{candidate_id}",
#     response_model=CandidateRead,
#     tags=["candidats"],
# )
def get_candidate(
    candidate_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> CandidateDto:
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
) -> CandidateDto:
    """Retrieve the candidate entity bound to a specific user account."""
    candidate = CandidateService(db).get_candidate_by_user(user_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate
