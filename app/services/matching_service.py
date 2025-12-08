from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.offer_repository import OfferRepository
from app.schemas import MatchingScoreResponse


LANGUAGE_ALIASES = {
    "french": "fr",
    "francais": "fr",
    "français": "fr",
    "anglais": "en",
    "english": "en",
    "espagnol": "es",
    "spanish": "es",
    "allemand": "de",
    "german": "de",
    "portugais": "pt",
    "portuguese": "pt",
}

SENIORITY_KEYWORDS = {
    "intern": "intern",
    "junior": "junior",
    "beginner": "beginner",
    "intermediate": "intermediate",
    "confirmed": "intermediate",
    "advanced": "advanced",
    "senior": "senior",
    "lead": "senior",
    "expert": "expert",
}


@dataclass(frozen=True)
class MatchingWeights:
    coverage: float = 0.30
    title_similarity: float = 0.20
    geo_fit: float = 0.15
    seniority: float = 0.10
    language: float = 0.10
    salary: float = 0.10
    profile_focus: float = 0.05

    def as_dict(self) -> dict[str, float]:
        values = self.__dict__
        total = sum(values.values()) or 1
        return {key: weight / total for key, weight in values.items()}


class MatchingService:
    """Compute compatibility scores between candidates and job offers."""

    def __init__(self, db: Session, weights: MatchingWeights | None = None):
        self.candidates = CandidateRepository(db)
        self.offers = OfferRepository(db)
        self.weights = (weights or MatchingWeights()).as_dict()

    def score_candidate_for_offer(
        self,
        candidate_id: UUID,
        offer_id: UUID,
    ) -> MatchingScoreResponse | None:
        candidate = self.candidates.get(candidate_id)
        offer = self.offers.get(offer_id)
        if candidate is None or offer is None:
            return None

        score, matched_skills = self._score_candidate(candidate, offer)
        return MatchingScoreResponse(score=round(score, 4), matched_skills=matched_skills)

    def rank_candidates_for_offer(
        self,
        offer_id: UUID,
        limit: int = 10,
    ) -> list[dict] | None:
        offer = self.offers.get(offer_id)
        if offer is None:
            return None

        candidates = self.candidates.list()
        scored_results: list[dict] = []
        for candidate in candidates:
            score, matched_skills = self._score_candidate(candidate, offer)
            scored_results.append(
                {
                    "candidate": candidate,
                    "score": round(score, 4),
                    "matched_skills": matched_skills,
                }
            )

        scored_results.sort(key=lambda item: item["score"], reverse=True)
        return scored_results[:limit]

    # ------------------------------------------------------------------
    # Component builders
    # ------------------------------------------------------------------
    def _compute_components(self, candidate, offer) -> tuple[dict[str, float], list[str]]:
        offer_skills, offer_skill_map = self._extract_offer_skills(offer)
        candidate_skills = self._extract_candidate_skills(candidate)

        overlap = offer_skills & candidate_skills
        matched_skills = sorted(offer_skill_map[key] for key in overlap)

        coverage = len(overlap) / len(offer_skills) if offer_skills else 0.0
        profile_focus = (
            len(overlap) / len(offer_skills | candidate_skills)
            if offer_skills or candidate_skills
            else 0.0
        )

        components = {
            "coverage": coverage,
            "title_similarity": self._title_similarity(candidate, offer),
            "geo_fit": self._geo_fit(candidate, offer),
            "seniority": self._seniority_fit(candidate, offer),
            "language": self._language_fit(candidate, offer),
            "salary": self._salary_fit(candidate, offer),
            "profile_focus": profile_focus,
        }
        return components, matched_skills

    def _score_candidate(self, candidate, offer) -> tuple[float, list[str]]:
        components, matched_skills = self._compute_components(candidate, offer)
        score = sum(self.weights[name] * value for name, value in components.items())
        return score, matched_skills

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize(value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower()
        return normalized or None

    def _extract_candidate_skills(self, candidate) -> set[str]:
        normalized: set[str] = set()
        for skill in getattr(candidate, "skills", []) or []:
            name = self._normalize(getattr(skill, "name", None))
            if not name:
                continue
            normalized.add(name)
        return normalized

    def _extract_offer_skills(self, offer) -> tuple[set[str], dict[str, str]]:
        skill_map: dict[str, str] = {}
        for tag in getattr(offer, "tags", []) or []:
            name = self._normalize(getattr(tag, "name", None))
            if not name:
                continue
            skill_map[name] = tag.name.strip()
        return set(skill_map.keys()), skill_map

    # --- coverage & similarity ---
    def _title_similarity(self, candidate, offer) -> float:
        offer_title = self._normalize(getattr(offer, "title", None))
        candidate_titles = self._candidate_titles(candidate)
        
        candidate_text = " ".join(candidate_titles)
        if not offer_title or not candidate_text:
            return 0.0

        ratio = SequenceMatcher(None, offer_title, candidate_text.lower()).ratio()

        offer_tokens = set(self._tokenize(offer_title))
        candidate_tokens = set(self._tokenize(candidate_text))
        union = offer_tokens | candidate_tokens
        
        
        
        token_similarity = (len(offer_tokens & candidate_tokens) / len(union)) if union else 0.0
        
        result = 0.7 * ratio + 0.3 * token_similarity
        
        return result

    def _candidate_titles(self, candidate) -> list[str]:
        titles: list[str] = []
        pref = getattr(candidate, "job_preferences", None)
        raw_values = [
            getattr(candidate, "professional_title", None),
            getattr(pref, "desired_position", None) if pref else None,
        ]
        for exp in getattr(candidate, "experiences", []) or []:
            if len(titles) >= 3:
                break
            raw_values.append(getattr(exp, "position", None))

        for value in raw_values:
            if not value:
                continue
            text = value.strip()
            if text:
                titles.append(text)
        return titles

    @staticmethod
    def _tokenize(value: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", value.lower())

    # --- geographic fit ---
    def _geo_fit(self, candidate, offer) -> float:
        offer_country = self._normalize(getattr(offer, "work_country_location", None)).lower()
        offer_city = self._normalize(getattr(offer, "work_city_location", None)).lower()

        pref = getattr(candidate, "job_preferences", None)
        cand_country = self._normalize(getattr(pref, "country", None)) or self._normalize(
            getattr(candidate, "country", None)
        ).lower()
        # cand_region = self._normalize(getattr(pref, "region", None)) or self._normalize(
        #     getattr(candidate, "region", None)
        # )
        cand_city = self._normalize(getattr(pref, "city", None)) or self._normalize(
            getattr(candidate, "city", None)
        ).lower()
        score = 0.0
        if offer_city and cand_city and offer_city == cand_city:
            score = 1.0
        elif offer_country and offer_country == cand_country:
            score = 0.5
        
        return score

    # --- seniority / experience ---
    def _seniority_fit(self, candidate, offer) -> float:
        candidate_level = self._normalize(getattr(candidate, "experience_level", None))
        offer_level = self._infer_offer_seniority(offer)
        # print(offer)
        if candidate_level and offer_level:
            return 1.0 if candidate_level == offer_level else 0.3
        if candidate_level or offer_level:
            return 0.5
        return 0.4

    def _infer_offer_seniority(self, offer) -> str | None:
        for tag in getattr(offer, "tags", []) or []:
            normalized = self._normalize(getattr(tag, "name", None))
            if not normalized:
                continue
            mapped = SENIORITY_KEYWORDS.get(normalized)
            if mapped:
                return mapped

        for text in (getattr(offer, "title", None), getattr(offer, "description", None)):
            if not text:
                continue
            for token in self._tokenize(text):
                mapped = SENIORITY_KEYWORDS.get(token)
                if mapped:
                    return mapped
        return None

    # --- languages ---
    def _language_fit(self, candidate, offer) -> float:
        candidate_languages = self._candidate_languages(candidate)
        required_languages = self._offer_languages(offer)
        
        if not required_languages:
            return 1.0
        if not candidate_languages:
            return 0.0
        matches = candidate_languages & required_languages
        
        return len(matches) / len(required_languages)

    def _candidate_languages(self, candidate) -> set[str]:
        normalized: set[str] = set()
        for language in getattr(candidate, "languages", []) or []:
            name = self._normalize(getattr(language, "language", None))
            if not name:
                continue
            normalized_code = LANGUAGE_ALIASES.get(name, name)
            normalized.add(normalized_code)
        return normalized

    def _offer_languages(self, offer) -> set[str]:
        normalized: set[str] = set()
        for tag in getattr(offer, "tags", []) or []:
            name = self._normalize(getattr(tag, "name", None))
            if not name:
                continue
            code = LANGUAGE_ALIASES.get(name)
            if code:
                normalized.add(code)

        explicit_required = self._normalize(getattr(offer, "required_language", None))
        if explicit_required:
            normalized.add(LANGUAGE_ALIASES.get(explicit_required, explicit_required))

        description = getattr(offer, "description", None)
        title = getattr(offer, "title", None)
        for text in (description, title):
            if not text:
                continue
            for token in self._tokenize(text):
                code = LANGUAGE_ALIASES.get(token)
                if code:
                    normalized.add(code)
        return normalized

    # --- salary fit ---
    def _salary_fit(self, candidate, offer) -> float:
        expectation = self._parse_salary_expectation(candidate)
        offer_min, offer_max = self._parse_salary_range(getattr(offer, "salary", None))
        if expectation is None or (offer_min is None and offer_max is None):
            return 0.5

        min_salary = offer_min or offer_max or expectation
        max_salary = offer_max or min_salary
        if min_salary <= expectation <= max_salary:
            return 1.0

        if expectation < min_salary:
            diff_ratio = (min_salary - expectation) / max(min_salary, 1)
        else:
            diff_ratio = (expectation - max_salary) / max(max_salary, 1)

        return max(0.0, 1.0 - diff_ratio)

    def _parse_salary_expectation(self, candidate) -> float | None:
        pref = getattr(candidate, "job_preferences", None)
        if pref is None:
            return None
        raw_value = getattr(pref, "pretentions_salarial", None)
        if not raw_value:
            return None
        digits = re.findall(r"\d+(?:[.,]\d+)?", raw_value.replace(" ", ""))
        if not digits:
            return None
        normalized = digits[0].replace(",", ".")
        try:
            return float(normalized)
        except ValueError:
            return None

    @staticmethod
    def _parse_salary_range(raw_value: str | None) -> tuple[float | None, float | None]:
        if not raw_value:
            return (None, None)
        digits = re.findall(r"\d+(?:[.,]\d+)?", raw_value.replace(" ", ""))
        values: list[float] = []
        for entry in digits[:2]:
            normalized = entry.replace(",", ".")
            try:
                values.append(float(normalized))
            except ValueError:
                continue
        if not values:
            return (None, None)
        if len(values) == 1:
            return (values[0], None)
        first, second = values[:2]
        return (min(first, second), max(first, second))
