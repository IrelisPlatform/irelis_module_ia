from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

<<<<<<< ours
from sqlalchemy import or_, text

from app.models import Candidate, JobPreferences, JobPreferencesContractType, JobPreferencesSector, Language
from app.models.enums import ContractType, ExperienceLevel
from app.utils.bool_to_sql import build_boolean_filter
=======
from app.models import Candidate, JobPreferences, JobPreferencesSector

>>>>>>> theirs

class CandidateRepository:
    """Data access helpers for candidate entities."""

    def __init__(self, db: Session):
        self.db = db

    def _query_with_relationships(self):
        return self.db.query(Candidate).options(
            selectinload(Candidate.skills),
            selectinload(Candidate.languages),
            selectinload(Candidate.educations),
            selectinload(Candidate.experiences),
            selectinload(Candidate.job_preferences),
            selectinload(Candidate.applications),
            selectinload(Candidate.saved_job_offers),
        )

    def list(self) -> list[Candidate]:
        return self._query_with_relationships().all()

    def get(self, candidate_id: UUID) -> Candidate | None:
        return (
            self._query_with_relationships()
            .filter(Candidate.id == candidate_id)
            .first()
        )
    
    def get_by_user_id(self, user_id: UUID) -> Candidate | None:
        return (
            self._query_with_relationships()
            .filter(Candidate.user_id == user_id)
            .first()
        )
<<<<<<< ours

    def search(
        self,
        query_text: str | None = None,
        city: str | None = None,
        town: str | None = None,
        country: str | None = None,
        contract_type: ContractType | None = None,
        school_level: str | None = None,
        experience_level: ExperienceLevel | None = None,
        language: str | None = None,
        bool_mode: bool = False,
    ) -> list[Candidate]:
        query = self._query_with_relationships()
        query = self._apply_query_text(query, query_text, bool_mode)
        if city:
            query = query.filter(Candidate.city.ilike(f"%{city}%"))
        if town:
            query = query.filter(Candidate.region.ilike(f"%{town}%"))
        if country:
            query = query.filter(Candidate.country.ilike(f"%{country}%"))
        if school_level:
            query = query.filter(Candidate.school_level.ilike(f"%{school_level}%"))
        if experience_level:
            query = query.filter(Candidate.experience_level == experience_level.value)
        if contract_type:
            query = query.filter(
                Candidate.job_preferences.has(
                    JobPreferencesContractType.contract_type == contract_type
                )
            )
        if language:
            query = query.filter(
                Candidate.languages.any(Language.language.ilike(f"%{language}%"))
            )
        return query.all()

    def _apply_query_text(
        self,
        query,
        query_text: str | None,
        bool_mode: bool,
    ):
        if not query_text:
            return query
        query_text = query_text.strip()
        if not query_text:
            return query
        if bool_mode:
            try:
                where_sql, params = build_boolean_filter(query_text)
            except ValueError:
                tokens = [token.strip() for token in query_text.split() if token.strip()]
                for token in tokens:
                    pattern = f"%{token}%"
                    query = query.filter(
                        or_(
                            Candidate.first_name.ilike(pattern),
                            Candidate.last_name.ilike(pattern),
                            Candidate.professional_title.ilike(pattern),
                        )
                    )
                return query
            clause = text(where_sql).params(**params)
            query = query.filter(clause)
        else:
            pattern = f"%{query_text}%"
            query = query.filter(
                or_(
                    Candidate.first_name.ilike(pattern),
                    Candidate.last_name.ilike(pattern),
                    Candidate.professional_title.ilike(pattern),
                )
            )
        return query
=======
>>>>>>> theirs
