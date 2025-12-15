from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, selectinload

from app.models import Candidate, JobOffer, Search, Tag
from app.models.enums import SearchTarget, SearchType
from app.utils.search_filters import (
    apply_text_search,
    as_list,
    enum_to_str,
    list_to_csv,
    normalize,
    parse_datetime,
)

if TYPE_CHECKING:
    from app.schemas import SearchCreate


class SearchRepository:
    """Data access helpers dedicated to searching job offers."""

    def __init__(self, db: Session):
        """Store session for reuse."""
        self.db = db

    def _query(self):
        """Base query returning offers with needed relationships."""
        return self.db.query(JobOffer).options(
            selectinload(JobOffer.recruiter),
            selectinload(JobOffer.applications),
            selectinload(JobOffer.tags),
        )

    def search_for_candidate(
        self,
        candidate: Candidate,
        search_filters: dict | None = None,
    ) -> list[JobOffer]:
        """Search offers using candidate data combined with optional filters."""
        filters = search_filters or {}
        query = self._query()

        query = apply_text_search(query, filters.get("query"))

        candidate_preferences = getattr(candidate, "job_preferences", None)

        contract_filter = (
            filters.get("type_contrat")
            or filters.get("contract_type")
        )
        if not contract_filter and candidate_preferences and candidate_preferences.contract_types:
            contract_filter = [
                pref.contract_type
                for pref in candidate_preferences.contract_types
                if pref.contract_type
            ]
        contract_values = as_list(contract_filter)
        if contract_values:
            query = query.filter(JobOffer.contract_type.in_(contract_values))

        country = filters.get("country")
        if not country and candidate_preferences and candidate_preferences.country:
            country = candidate_preferences.country
        if not country:
            country = candidate.country
        if country:
            normalized_country = normalize(country)
            query = query.filter(func.lower(JobOffer.work_country_location) == normalized_country)

        city = filters.get("city")
        if not city and candidate_preferences and candidate_preferences.city:
            city = candidate_preferences.city
        if not city:
            city = candidate.city
        if city:
            normalized_city = normalize(city)
            query = query.filter(func.lower(JobOffer.work_city_location) == normalized_city)

        skill_names = filters.get("skills")
        if not skill_names:
            skill_names = [
                skill.name for skill in getattr(candidate, "skills", []) if skill.name
            ]
        skill_values = as_list(skill_names)
        if skill_values:
            normalized_skills = [normalize(skill) for skill in skill_values if skill]
            if normalized_skills:
                query = query.filter(
                    JobOffer.tags.any(func.lower(Tag.name).in_(normalized_skills))
                )

        date_publication = parse_datetime(filters.get("date_publication"))
        if date_publication:
            query = query.filter(JobOffer.published_at >= date_publication)

        language = filters.get("language")
        if language:
            like_language = f"%{language}%"
            query = query.filter(
                or_(
                    JobOffer.title.ilike(like_language),
                    JobOffer.description.ilike(like_language),
                    JobOffer.required_language.ilike(like_language),
                )
            )

        return query.all()

    def search_by_payload(self, payload: "SearchCreate") -> list[JobOffer]:
        """Search offers using the provided payload filters only."""
        query = self._query()
        
        query = apply_text_search(query, getattr(payload, "query", None))

        country = getattr(payload, "country", None)
        
        if country:
            normalized_country = normalize(country)
            query = query.filter(func.lower(JobOffer.work_country_location) == normalized_country)

        city = getattr(payload, "city", None)
        if city:
            normalized_city = normalize(city)
            query = query.filter(func.lower(JobOffer.work_city_location) == normalized_city)

        contract_type = getattr(payload, "type_contrat", None) or getattr(payload, "contract_type", None)
        contract_values = as_list(contract_type)
        if contract_values:
            query = query.filter(JobOffer.contract_type.in_(contract_values))

        language = getattr(payload, "language", None)
        if language:
            like_language = f"%{language}%"
            query = query.filter(
                or_(
                    JobOffer.title.ilike(like_language),
                    JobOffer.description.ilike(like_language),
                    JobOffer.required_language.ilike(like_language),
                )
            )

        date_publication = parse_datetime(getattr(payload, "date_publication", None))
        if date_publication:
            query = query.filter(JobOffer.published_at >= date_publication)

        
        return query.all()

    def record_search(self, user_id: UUID, payload: "SearchCreate" | None) -> None:
        """Persist the search payload for later analytics."""
        search_type = SearchType.BOOL
        target = SearchTarget.OFFRE
        query_text = ""
        country = city = town = None
        type_contrat = None
        niveau_etude = None
        experience = None
        language = None
        date_publication = None

        if payload is not None:
            search_type = payload.type or SearchType.BOOL
            target = payload.target or SearchTarget.OFFRE
            query_text = payload.query or ""
            country = payload.country
            city = payload.city
            town = payload.town
            type_contrat = payload.type_contrat or payload.contract_type
            niveau_etude = payload.niveau_etude or payload.school_level
            experience = payload.experience or payload.experience_level
            language = payload.language
            date_publication = payload.date_publication

        search_entry = Search(
            query=query_text,
            type=search_type,
            target=target,
            country=country,
            city=city,
            town=town,
            type_contrat=list_to_csv(type_contrat),
            niveau_etude=enum_to_str(niveau_etude),
            experience=enum_to_str(experience),
            language=language,
            date_publication=date_publication,
            user_id=user_id,
        )
        self.db.add(search_entry)
        self.db.commit()
