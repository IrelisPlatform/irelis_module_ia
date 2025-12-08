from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import CandidateMatch, SourcingSearchResponse
from app.services.matching_service import MatchingService


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
    service = MatchingService(db)
    ranked = service.rank_candidates_for_offer(offer_id, limit)
    if ranked is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre introuvable",
        )

    candidates: list[CandidateMatch] = []
    for entry in ranked:
        candidate = entry["candidate"]
        skills = entry["matched_skills"] or _candidate_skill_names(candidate)
        candidates.append(
            CandidateMatch(
                id=candidate.id,
                name=_candidate_full_name(candidate),
                score=entry["score"],
                location=_candidate_location(candidate),
                skills=skills,
            )
        )

    return SourcingSearchResponse(candidates=candidates)


def _candidate_full_name(candidate) -> str:
    first = (getattr(candidate, "first_name", "") or "").strip()
    last = (getattr(candidate, "last_name", "") or "").strip()
    full_name = f"{first} {last}".strip()
    if full_name:
        return full_name
    return getattr(candidate, "professional_title", None) or "Profil anonyme"


def _candidate_location(candidate) -> str | None:
    city = getattr(candidate, "city", None)
    region = getattr(candidate, "region", None)
    country = getattr(candidate, "country", None)
    for part in (city, region, country):
        if part:
            return part
    return None


def _candidate_skill_names(candidate) -> list[str]:
    names: list[str] = []
    for skill in getattr(candidate, "skills", []) or []:
        title = getattr(skill, "name", None)
        if title:
            names.append(title)
    return names
