from __future__ import annotations

from ast import stmt
from uuid import UUID

from sqlalchemy import String, cast, or_, and_
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

    def search_by_boolean_query(self, query: str, page: int, size: int) -> tuple[int, list[Candidate]]:
        """Recherche booléenne avec pagination."""
        expression = self._boolean_parser.build_expression(query, self._term_clause)
        if expression is None:
            return 0, []
            
        query_filtered = self._query_with_relationships().filter(expression)
        
        total_elements = query_filtered.count()
        offset = (page - 1) * size
        candidates = query_filtered.offset(offset).limit(size).all()
        
        return total_elements, candidates

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
                    # JobPreferences.region.ilike(like_term),
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
            # Candidate.region.ilike(like_term),
            Candidate.phone_number.ilike(like_term),
            Candidate.portfolio_url.ilike(like_term),
            Candidate.linked_in_url.ilike(like_term),
        )

        clauses = [direct_fields, experience_clause, education_clause, language_clause, skill_clause]
        clauses.extend(job_pref_conditions)

        return or_(*clauses)
    
    
    def search_candidates_by_keywords(self, query: str, page: int, size: int) -> tuple[int, list[Candidate]]:
        """Search candidates using standard multi-column keyword matching."""
        
        # 1. Nettoyer et découper la requête en mots-clés
        # Exemple: "Developpeur Python Paris" -> ["Developpeur", "Python", "Paris"]
        tokens = query.strip().split()
        if not tokens:
            return []

        # 2. Préparer la requête de base (avec les chargements de relations habituels)
        stmt = self._query_with_relationships()

        # 3. Construire les conditions dynamiques
        # On veut que CHAQUE mot-clé soit trouvé au moins quelque part (AND global)
        conditions = []
        for token in tokens:
            search_term = f"%{token}%"
            
            # Le mot-clé peut être dans le titre, le nom, la ville, les skills OU les expériences
            token_condition = or_(
                Candidate.professional_title.ilike(search_term),
                Candidate.first_name.ilike(search_term),
                Candidate.last_name.ilike(search_term),
                Candidate.city.ilike(search_term),
                Candidate.country.ilike(search_term),
                Candidate.presentation.ilike(search_term),
                Candidate.skills.any(Skill.name.ilike(search_term)),
                Candidate.experiences.any(Experience.position.ilike(search_term)),
                Candidate.experiences.any(Experience.description.ilike(search_term)),
                Candidate.experiences.any(Experience.company_name.ilike(search_term))
            )
            conditions.append(token_condition)
            query_filtered = stmt.filter(and_(*conditions))
            total_elements = query_filtered.count()
            
        offset = (page - 1) * size
        candidates = query_filtered.offset(offset).limit(size).all()
    
        return total_elements, candidates
