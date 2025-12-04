from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import JobOfferRead, SearchCreate
from app.services.search_service import SearchService
from app.models.enums import (
    ContractType,
    ExperienceLevel,
    SchoolLevel,
    SearchTarget,
    SearchType,
)

router = APIRouter()

def _parse_search_filters(
    query: str | None = Query(default=None),
    search_type: SearchType | None = Query(default=None, alias="type"),
    target: SearchTarget | None = Query(default=None),
    country: str | None = Query(default=None),
    city: str | None = Query(default=None),
    town: str | None = Query(default=None),
    type_contrat: list[ContractType] | ContractType | None = Query(default=None),
    contract_type: list[ContractType] | ContractType | None = Query(default=None),
    niveau_etude: SchoolLevel | None = Query(default=None),
    school_level: SchoolLevel | None = Query(default=None),
    experience: ExperienceLevel | None = Query(default=None),
    experience_level: ExperienceLevel | None = Query(default=None),
    language: str | None = Query(default=None),
    date_publication: datetime | None = Query(default=None),
    skills: list[str] | None = Query(default=None),
) -> SearchCreate:
    def _to_list(value):
        if value is None:
            return None
        if isinstance(value, list):
            return value
        return [value]

    return SearchCreate(
        query=query,
        type=search_type,
        target=target,
        country=country,
        city=city,
        town=town,
        type_contrat=_to_list(type_contrat),
        contract_type=_to_list(contract_type),
        niveau_etude=niveau_etude,
        school_level=school_level,
        experience=experience,
        experience_level=experience_level,
        language=language,
        date_publication=date_publication,
        skills=skills,
    )

SearchFilters = Annotated[SearchCreate, Depends(_parse_search_filters)]

@router.get(
    "/recherches/offres",
    response_model=list[JobOfferRead],
    tags=["recherches"],
)
def search_offers(
    db: Annotated[Session, Depends(deps.get_db)],
    filters: SearchFilters,
    user_id: UUID | None = Query(default=None),
) -> list[JobOfferRead]:
    service = SearchService(db)
    if user_id is None:
        return service.search_by_payload(filters)

    payload_data = filters if filters.model_dump(exclude_none=True) else None
    offers = service.search_for_candidate_by_user(user_id, payload_data)
    if offers is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidat introuvable",
        )
    return offers
