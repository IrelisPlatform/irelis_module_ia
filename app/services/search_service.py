from __future__ import annotations

import re
import unicodedata
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.offer_repository import OfferRepository
from app.repositories.search_repository import SearchRepository
from app.schemas import OfferRead, SearchBase, SearchCreate, SearchRead
from app.models.enums import Mobility


class SearchService:
    def __init__(self, db: Session):
        self.repo = SearchRepository(db)
        self.offer_repo = OfferRepository(db)
        self.candidate_repo = CandidateRepository(db)

    def list_searches(self) -> list[SearchRead]:
        return [SearchRead.model_validate(s) for s in self.repo.list()]

    def get_search(self, search_id: UUID) -> SearchRead | None:
        search = self.repo.get(search_id)
        if search is None:
            return None
        return SearchRead.model_validate(search)

    def list_by_user(self, user_id: UUID) -> list[SearchRead]:
        return [
            SearchRead.model_validate(s)
            for s in self.repo.list_by_user(user_id)
        ]

    def execute_search(self, payload: SearchBase, user_id: UUID | None = None) -> list[OfferRead]:
        stored_payload: SearchBase | SearchCreate = payload
        compatibility_scores: dict[UUID, float] = {}

        if user_id:
            stored_payload = SearchCreate(
                user_id=user_id,
                **payload.model_dump(),
            )
            self.repo.create(stored_payload)

        offers = self.offer_repo.search_by_payload(stored_payload)

        candidate = self.candidate_repo.get_by_user_id(user_id) if user_id else None
        if candidate:
            offers, compatibility_scores = self._sort_offers_by_candidate_score(candidate, offers)

        enriched_offers: list[OfferRead] = []
        for offer in offers:
            offer_read = OfferRead.model_validate(offer)
            score = compatibility_scores.get(getattr(offer, "id"))
            if score is not None:
                offer_read = offer_read.model_copy(update={"compatibility_score": score})
            enriched_offers.append(offer_read)
        return enriched_offers

    def _sort_offers_by_candidate_score(self, candidate, offers):
        compatibility_scores = {
            offer.id: self._compute_candidate_offer_score(candidate, offer)
            for offer in offers
        }
        sorted_offers = sorted(offers, key=lambda offer: compatibility_scores[offer.id], reverse=True)
        return sorted_offers, compatibility_scores

    def _compute_candidate_offer_score(self, candidate, offer) -> float:
        weights = {
            "coverage": 0.25,
            "title": 0.2,
            "geo": 0.2,
            "seniority": 0.1,
            "language": 0.1,
            "salary": 0.15,
        }

        coverage = self._skill_coverage(candidate, offer)
        title_similarity = self._title_similarity(candidate, offer)
        geo_fit = self._geo_fit(candidate, offer)
        seniority_fit = self._seniority_fit(candidate, offer)
        language_fit = self._language_fit(candidate, offer)
        salary_fit = self._salary_fit(candidate, offer)

        score = (
            (coverage * weights["coverage"])
            + (title_similarity * weights["title"])
            + (geo_fit * weights["geo"])
            + (seniority_fit * weights["seniority"])
            + (language_fit * weights["language"])
            + (salary_fit * weights["salary"])
        )
        return round(score * 100, 2)

    def _skill_coverage(self, candidate, offer) -> float:
        candidate_skills = {
            skill.title.strip().lower()
            for skill in getattr(candidate, "skills", [])
            if getattr(skill, "title", None)
        }
        offer_skills = {
            skill.title.strip().lower()
            for skill in getattr(offer, "skills", [])
            if getattr(skill, "title", None)
        }
        if not offer_skills:
            return 0.5
        matched_skills = candidate_skills.intersection(offer_skills)
        return len(matched_skills) / len(offer_skills)

    def _title_similarity(self, candidate, offer) -> float:
        offer_tokens = self._tokenize_text(getattr(offer, "title", ""))
        if not offer_tokens:
            return 0.0
        best = 0.0
        for desired in getattr(candidate, "desired_positions", []):
            desired_tokens = self._tokenize_text(getattr(desired, "title", ""))
            if not desired_tokens:
                continue
            intersection = offer_tokens.intersection(desired_tokens)
            union = offer_tokens.union(desired_tokens)
            if union:
                best = max(best, len(intersection) / len(union))
        return best

    def _geo_fit(self, candidate, offer) -> float:
        score = 0.0
        candidate_country = getattr(candidate, "country", None)
        offer_country = getattr(offer, "country", None)
        if candidate_country and offer_country and candidate_country.lower() == offer_country.lower():
            score += 0.5

        candidate_city = getattr(candidate, "city", None)
        offer_city = getattr(offer, "city", None)
        if candidate_city and offer_city and candidate_city.lower() == offer_city.lower():
            score += 0.3

        score += 0.2 * self._mobility_match_score(getattr(candidate, "mobility", None), getattr(offer, "mobility", None))
        return min(score, 1.0)

    def _seniority_fit(self, candidate, offer) -> float:
        offer_seniority = getattr(offer, "seniority", None)
        if offer_seniority is None:
            return 0.5
        candidate_seniorities = {
            desired.level for desired in getattr(candidate, "desired_positions", []) if getattr(desired, "level", None)
        }
        if not candidate_seniorities:
            return 0.5
        return 1.0 if offer_seniority in candidate_seniorities else 0.0

    def _language_fit(self, candidate, offer) -> float:
        offer_language = getattr(offer, "language", None)
        if not offer_language:
            return 0.5
        candidate_languages = {
            lang.title.strip().lower()
            for lang in getattr(candidate, "languages", [])
            if getattr(lang, "title", None)
        }
        if not candidate_languages:
            return 0.5
        return 1.0 if offer_language.strip().lower() in candidate_languages else 0.0

    def _salary_fit(self, candidate, offer) -> float:
        candidate_range = self._extract_salary_bounds(candidate)
        offer_range = self._extract_salary_bounds(offer)
        if not candidate_range or not offer_range:
            return 0.5
        cand_min, cand_max = candidate_range
        offer_min, offer_max = offer_range

        overlap_min = max(cand_min, offer_min)
        overlap_max = min(cand_max, offer_max)
        if overlap_min > overlap_max:
            return 0.0
        total_span = max(cand_max, offer_max) - min(cand_min, offer_min)
        if total_span == 0:
            return 1.0
        overlap = overlap_max - overlap_min
        return overlap / total_span

    def _mobility_match_score(self, candidate_mobility, offer_mobility) -> float:
        if candidate_mobility is None or offer_mobility is None:
            return 0.5
        allowed = {candidate_mobility}
        if candidate_mobility == Mobility.REMOTE:
            allowed.add(Mobility.HYBRID)
        elif candidate_mobility == Mobility.ON_SITE:
            allowed.add(Mobility.HYBRID)
        elif candidate_mobility == Mobility.HYBRID:
            allowed.update({Mobility.REMOTE, Mobility.ON_SITE})
        return 1.0 if offer_mobility in allowed else 0.0

    def _extract_salary_bounds(self, entity) -> tuple[float, float] | None:
        salary_min = self._to_float(getattr(entity, "salary_min", None))
        salary_max = self._to_float(getattr(entity, "salary_max", None))
        salary_avg = self._to_float(getattr(entity, "salary_avg", None))

        if salary_min is None and salary_avg is not None:
            salary_min = salary_avg
        if salary_max is None and salary_avg is not None:
            salary_max = salary_avg
        if salary_min is None or salary_max is None:
            return None
        if salary_min > salary_max:
            salary_min, salary_max = salary_max, salary_min
        return salary_min, salary_max

    def _tokenize_text(self, text: str) -> set[str]:
        if not text:
            return set()
        normalized = unicodedata.normalize("NFKD", text)
        ascii_text = "".join(ch for ch in normalized if not unicodedata.combining(ch)).lower()
        return set(re.findall(r"\b\w+\b", ascii_text))

    def _to_float(self, value) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
