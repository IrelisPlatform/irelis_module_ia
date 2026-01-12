from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import JobOfferSearchResponse, SearchCreate
from app.services.search_service import SearchService
from app.models.enums import (
    ContractType,
    ExperienceLevel,
    SchoolLevel,
    SearchTarget,
    SearchType,
)

router = APIRouter()

def _parse_search_offes_filters(
    query: str | None = Query(default=None),
    country: str | None = Query(default=None),
    city: str | None = Query(default=None),
    town: str | None = Query(default=None),
    contract_type: list[ContractType] | ContractType | None = Query(default=None),
    niveau_etude: SchoolLevel | None = Query(default=None),
    experience: ExperienceLevel | None = Query(default=None),
    language: str | None = Query(default=None),
    date_publication: datetime | None = Query(default=None)
) -> SearchCreate:
    """Normalize incoming query parameters into a SearchCreate schema."""
    def _to_list(value):
        """Return the provided query parameter as a list."""
        if value is None:
            return None
        if isinstance(value, list):
            return value
        return [value]

    return SearchCreate(
        query=query,
        type=SearchType.NOT,
        target=SearchTarget.OFFRE,
        country=country,
        city=city,
        town=town,
        contract_type=_to_list(contract_type),
        niveau_etude=niveau_etude,
        experience=experience,
        language=language,
        date_publication=date_publication,
    )

SearchFilters = Annotated[SearchCreate, Depends(_parse_search_offes_filters)]

@router.get(
    "/recherches/offres",
    response_model=JobOfferSearchResponse,
    tags=["recherches"],
)
def search_offers(
    db: Annotated[Session, Depends(deps.get_db)],
    filters: SearchFilters,
    user_id: UUID | None = Query(default=None),
    page: int = Query(default=0, ge=0),
    size: int = Query(default=0, ge=0),
) -> JobOfferSearchResponse:
    """Search job offers by payload or contextually for a candidate."""
    
    service = SearchService(db)
    if user_id is None:
        offers = service.search_by_payload(filters)
    else:
        offers = service.search_for_candidate_by_user(user_id, filters)

        if offers is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidat introuvable",
            )

    total_elements = len(offers)
    if size <= 0:
        paged_offers = offers
        total_pages = 0 if total_elements == 0 else 1
        first = True
        last = True
    else:
        start = page * size
        end = start + size
        paged_offers = offers[start:end]
        total_pages = (total_elements + size - 1) // size
        first = page == 0
        last = page >= max(total_pages - 1, 0)

    return JobOfferSearchResponse(
        content=paged_offers,
        page=page,
        size=size,
        total_elements=total_elements,
        total_pages=total_pages,
        first=first,
        last=last,
    )
