from __future__ import annotations

from typing import Annotated
from uuid import UUID

from app.schemas.entities import CandidateSearchResponse
from app.schemas.entities import CandidateSearchResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import CandidateDto
from app.services.candidate_service import CandidateService
from app.utils.cache import APP_CACHE, make_cache_key

router = APIRouter()


@router.get("", response_model=list[CandidateDto], tags=["candidats"])
def list_candidates(
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[CandidateDto]:
    """Return every candidate profile."""
    cache_key = make_cache_key("list_candidates")
    cached = APP_CACHE.get(cache_key)
    if cached[0]:
        return cached[1]
    results = CandidateService(db).list_candidates()
    APP_CACHE.set(cache_key, results)
    return results


@router.get(
    "/recherche/bool",
    response_model=CandidateSearchResponse,
    tags=["candidats"],
)
def boolean_search_candidates(
    db: Annotated[Session, Depends(deps.get_db)],
    user_id: UUID = Query(..., description="Identifiant du recruteur"),
    query: str = Query(..., min_length=1, description="Requête booléenne"),
    page: int = Query(1, ge=1, description="Numéro de la page (commence à 1)"),
    size: int = Query(10, ge=1, le=100, description="Nombre d'éléments par page"),
) -> CandidateSearchResponse:
    """Search candidates using boolean operators and nested expressions."""
    # cache_key = make_cache_key("boolean_search_candidates", user_id, query)
    # cached = APP_CACHE.get(cache_key)
    # if cached[0]:
    #     return cached[1]
    service = CandidateService(db)
    try:
        results = service.search_by_boolean_query(query=query, user_id=user_id, page=page, size=size)
        # APP_CACHE.set(cache_key, results)
        return results
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

@router.get(
    "/recherche",
    response_model=CandidateSearchResponse,
    tags=["candidats"],
)
def normal_search_candidates(
    db: Annotated[Session, Depends(deps.get_db)],
    user_id: UUID = Query(..., description="Identifiant du recruteur"),
    query: str = Query(..., min_length=1, description="Requête par mots-clés"),
    page: int = Query(1, ge=1, description="Numéro de la page (commence à 1)"),
    size: int = Query(10, ge=1, le=100, description="Nombre d'éléments par page"),
) -> CandidateSearchResponse:
    """Search candidates using simple keywords across all profile fields."""
    
    # cache_key = make_cache_key("normal_search_candidates", user_id, query)
    # cached = APP_CACHE.get(cache_key)
    
    # Vérification du cache selon ton format actuel (found, value)
    # if cached and cached[0]:
    #     return cached[1]
        
    service = CandidateService(db)
    
    try:
        results = service.search_by_normal_query(query=query, user_id=user_id, page=page, size=size)
        # APP_CACHE.set(cache_key, results) 
        return results
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
