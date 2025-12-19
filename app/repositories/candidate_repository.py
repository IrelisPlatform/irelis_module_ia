from __future__ import annotations

from uuid import UUID

from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session, selectinload

from app.models import (
    Candidate,
    Education,
    Experience,
    JobPreferences,
    JobPreferencesContractType,
    JobPreferencesSector,
    Language,
    Sector,
    Skill,
)
from app.utils.boolean_query import BooleanQueryParser


class CandidateRepository:
    """Data access helpers for candidate entities."""

    def __init__(self, db: Session):
        """Store SQLAlchemy session for future queries."""
        self.db = db
        self._boolean_parser = BooleanQueryParser()

    def _query_with_relationships(self):
        """Base query including the relationships needed by services."""
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
        """Return all candidates with their relationships eagerly loaded."""
        return self._query_with_relationships().all()

    def get(self, candidate_id: UUID) -> Candidate | None:
        """Retrieve a candidate by identifier."""
        return (
            self._query_with_relationships()
            .filter(Candidate.id == candidate_id)
            .first()
        )

    def get_by_user_id(self, user_id: UUID) -> Candidate | None:
        """Retrieve the candidate linked to the provided user id."""
        return (
            self._query_with_relationships()
            .filter(Candidate.user_id == user_id)
            .first()
        )

    def search_by_boolean_query(self, query: str) -> list[Candidate]:
        """Search candidates matching the boolean expression supplied by the user."""
        expression = self._boolean_parser.build_expression(
            query, self._term_clause
        )
        if expression is None:
            return []
        return self._query_with_relationships().filter(expression).all()

    def _term_clause(self, raw_term: str):
        term = (raw_term or "").strip()
        if not term:
            return None

        like_term = term.replace("*", "%")
        if "%" not in like_term:
            like_term = f"%{like_term}%"
        like_term = like_term.replace("%%", "%")

        def _cast_like(column):
            return cast(column, String).ilike(like_term)

        job_pref_conditions = []
        job_pref_conditions.append(
            Candidate.job_preferences.has(
                or_(
                    JobPreferences.desired_position.ilike(like_term),
                    JobPreferences.city.ilike(like_term),
                    JobPreferences.country.ilike(like_term),
                    JobPreferences.region.ilike(like_term),
                    JobPreferences.availability.ilike(like_term),
                    JobPreferences.pretentions_salarial.ilike(like_term),
                )
            )
        )
        job_pref_conditions.append(
            Candidate.job_preferences.has(
                JobPreferences.sectors.any(
                    JobPreferencesSector.sector.has(Sector.name.ilike(like_term))
                )
            )
        )
        job_pref_conditions.append(
            Candidate.job_preferences.has(
                JobPreferences.contract_types.any(
                    _cast_like(JobPreferencesContractType.contract_type)
                )
            )
        )

        experience_clause = Candidate.experiences.any(
            or_(
                Experience.position.ilike(like_term),
                Experience.company_name.ilike(like_term),
                Experience.description.ilike(like_term),
                _cast_like(Experience.is_current),
            )
        )

        education_clause = Candidate.educations.any(
            or_(
                Education.institution.ilike(like_term),
                Education.degree.ilike(like_term),
                Education.city.ilike(like_term),
            )
        )

        language_clause = Candidate.languages.any(
            or_(
                Language.language.ilike(like_term),
                _cast_like(Language.level),
            )
        )

        skill_clause = Candidate.skills.any(
            or_(
                Skill.name.ilike(like_term),
                _cast_like(Skill.level),
            )
        )

        direct_fields = or_(
            Candidate.first_name.ilike(like_term),
            Candidate.last_name.ilike(like_term),
            Candidate.professional_title.ilike(like_term),
            Candidate.presentation.ilike(like_term),
            Candidate.pitch_mail.ilike(like_term),
            Candidate.city.ilike(like_term),
            Candidate.country.ilike(like_term),
            Candidate.region.ilike(like_term),
            Candidate.phone_number.ilike(like_term),
            Candidate.portfolio_url.ilike(like_term),
            Candidate.linked_in_url.ilike(like_term),
        )

        clauses = [direct_fields, experience_clause, education_clause, language_clause, skill_clause]
        clauses.extend(job_pref_conditions)

        return or_(*clauses)
