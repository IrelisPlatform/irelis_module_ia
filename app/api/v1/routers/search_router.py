from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.models.enums import PositionType, SearchTarget, SearchType
from app.schemas import OfferRead, SearchBase, SearchRead
from app.services.search_service import SearchService

router = APIRouter()


@router.get("/searches", response_model=list[SearchRead], tags=["searches"])
def list_searches(db: Annotated[Session, Depends(deps.get_db)]) -> list[SearchRead]:
    return SearchService(db).list_searches()


@router.get("/searches/{search_id}", response_model=SearchRead, tags=["searches"])
def get_search(
    search_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> SearchRead:
    search = SearchService(db).get_search(search_id)
    if search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search not found")
    return search


@router.get(
    "/users/{user_id}/searches",
    response_model=list[SearchRead],
    tags=["searches"],
)
def list_searches_by_user(
    user_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[SearchRead]:
    return SearchService(db).list_by_user(user_id)


@router.get(
    "/search/offers",
    response_model=list[OfferRead],
    tags=["searches", "offres"],
)
def execute_search(
    db: Annotated[Session, Depends(deps.get_db)],
    user_id: UUID | None = Query(
        default=None,
        description="Identifiant de l'utilisateur. "
        "Permet de lier la recherche et de prioriser les résultats pour un candidat.",
    ),
    query: str | None = Query(None, description="Texte libre, ex: 'CDI Développeur Backend'"),
    search_type: SearchType = Query(SearchType.DEFAULT, alias="type"),
    country: str | None = None,
    city: str | None = None,
    contract_type: PositionType | None = None,
) -> list[OfferRead]:
    if not query and not contract_type and not country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one search criterion (query/country/contract_type) is required.",
        )

    payload = SearchBase(
        query=query,
        type=search_type,
        target=SearchTarget.OFFER,
        country=country,
        city=city,
        contract_type=contract_type,
    )
    return SearchService(db).execute_search(payload, user_id=user_id)
