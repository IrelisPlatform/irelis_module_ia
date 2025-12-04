from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import or_, func
from sqlalchemy.orm import Session, selectinload

from app.models import Candidate, JobOffer, Tag

if TYPE_CHECKING:
    from app.schemas import SearchCreate


class SearchRepository:
    """Data access helpers dedicated to searching job offers."""

    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return self.db.query(JobOffer).options(
            selectinload(JobOffer.recruiter),
            selectinload(JobOffer.applications),
            selectinload(JobOffer.tags),
        )

    @staticmethod
    def _apply_text_search(query, raw_terms):
        if not raw_terms:
            return query

        if isinstance(raw_terms, str):
            terms = [term.strip() for term in raw_terms.split() if term.strip()]
        elif isinstance(raw_terms, (list, tuple, set)):
            terms = []
            for part in raw_terms:
                if not part:
                    continue
                terms.extend(
                    [sub.strip() for sub in str(part).split() if sub.strip()]
                )
        else:
            value = str(raw_terms).strip()
            terms = [value] if value else []

        if not terms:
            return query

        search_clauses = []
        for term in terms:
            like_term = f"%{term}%"
            search_clauses.append(
                or_(
                    JobOffer.title.ilike(like_term),
                    JobOffer.description.ilike(like_term),
                    JobOffer.tags.any(Tag.nom.ilike(like_term)),
                )
            )
        query = query.filter(or_(*search_clauses))
        return query

    @staticmethod
    def _as_list(value):
        if value is None:
            return []
        if isinstance(value, str):
            items = [item.strip() for item in value.split(",") if item.strip()]
            return items
        if isinstance(value, (list, tuple, set)):
            return [item for item in value if item]
        return [value]

    @staticmethod
    def _parse_datetime(value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return None

    @staticmethod
    def _normalize(value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().lower()

    def search_for_candidate(
        self,
        candidate: Candidate,
        search_filters: dict | None = None,
    ) -> list[JobOffer]:
        filters = search_filters or {}
        query = self._query()

        query = self._apply_text_search(query, filters.get("query"))

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
        contract_values = self._as_list(contract_filter)
        if contract_values:
            query = query.filter(JobOffer.contract_type.in_(contract_values))

        country = filters.get("country")
        if not country and candidate_preferences and candidate_preferences.country:
            country = candidate_preferences.country
        if not country:
            country = candidate.country
        if country:
            normalized_country = self._normalize(country)
            query = query.filter(func.lower(JobOffer.country) == normalized_country)

        city = filters.get("city")
        if not city and candidate_preferences and candidate_preferences.city:
            city = candidate_preferences.city
        if not city:
            city = candidate.city
        if city:
            normalized_city = self._normalize(city)
            query = query.filter(func.lower(JobOffer.city) == normalized_city)

        region = filters.get("town") or filters.get("region")
        if not region and candidate_preferences and candidate_preferences.region:
            region = candidate_preferences.region
        if not region:
            region = candidate.region
        if region:
            normalized_region = self._normalize(region)
            query = query.filter(func.lower(JobOffer.region) == normalized_region)

        skill_names = filters.get("skills")
        if not skill_names:
            skill_names = [
                skill.name for skill in getattr(candidate, "skills", []) if skill.name
            ]
        skill_values = self._as_list(skill_names)
        if skill_values:
            normalized_skills = [self._normalize(skill) for skill in skill_values if skill]
            if normalized_skills:
                query = query.filter(
                    JobOffer.tags.any(func.lower(Tag.nom).in_(normalized_skills))
                )

        experience = filters.get("experience") or filters.get("experience_level")
        if not experience:
            experience = getattr(candidate, "experience_level", None)
        if experience:
            query = query.filter(JobOffer.experience_level == experience)

        school_level = filters.get("niveau_etude") or filters.get("school_level")
        if not school_level:
            school_level = getattr(candidate, "school_level", None)
        if school_level:
            query = query.filter(JobOffer.school_level == school_level)

        date_publication = self._parse_datetime(filters.get("date_publication"))
        if date_publication:
            query = query.filter(JobOffer.published_at >= date_publication)

        language = filters.get("language")
        if language:
            like_language = f"%{language}%"
            query = query.filter(
                or_(
                    JobOffer.title.ilike(like_language),
                    JobOffer.description.ilike(like_language),
                )
            )

        return query.all()

    def search_by_payload(self, payload: "SearchCreate") -> list[JobOffer]:
        query = self._query()

        query = self._apply_text_search(query, getattr(payload, "query", None))

        country = getattr(payload, "country", None)
        if country:
            normalized_country = self._normalize(country)
            query = query.filter(func.lower(JobOffer.country) == normalized_country)

        city = getattr(payload, "city", None)
        if city:
            normalized_city = self._normalize(city)
            query = query.filter(func.lower(JobOffer.city) == normalized_city)

        town = getattr(payload, "town", None)
        if town:
            normalized_region = self._normalize(town)
            query = query.filter(func.lower(JobOffer.region) == normalized_region)

        contract_type = getattr(payload, "type_contrat", None) or getattr(payload, "contract_type", None)
        contract_values = self._as_list(contract_type)
        if contract_values:
            query = query.filter(JobOffer.contract_type.in_(contract_values))

        experience = getattr(payload, "experience", None) or getattr(payload, "experience_level", None)
        if experience:
            query = query.filter(JobOffer.experience_level == experience)

        school_level = getattr(payload, "niveau_etude", None) or getattr(payload, "school_level", None)
        if school_level:
            query = query.filter(JobOffer.school_level == school_level)

        language = getattr(payload, "language", None)
        if language:
            like_language = f"%{language}%"
            query = query.filter(
                or_(
                    JobOffer.title.ilike(like_language),
                    JobOffer.description.ilike(like_language),
                )
            )

        date_publication = self._parse_datetime(getattr(payload, "date_publication", None))
        if date_publication:
            query = query.filter(JobOffer.published_at >= date_publication)

        skill_names = getattr(payload, "skills", None)
        skill_values = self._as_list(skill_names)
        if skill_values:
            normalized_skills = [self._normalize(skill) for skill in skill_values if skill]
            if normalized_skills:
                query = query.filter(
                    JobOffer.tags.any(func.lower(Tag.nom).in_(normalized_skills))
                )

        return query.all()
