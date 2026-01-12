from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.offer_repository import OfferRepository
from app.schemas import (
    CandidateMatch,
    CandidateRecommendationsResponse,
    JobOfferMatch,
    JobOfferDto,
    MatchingScoreResponse,
    SourcingSearchResponse,
)
from app.services.dto_mappers import offer_to_dto


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
        """Return normalized weights that sum to 1."""
        values = self.__dict__
        total = sum(values.values()) or 1
        return {key: weight / total for key, weight in values.items()}


class MatchingService:
    """Compute compatibility scores between candidates and job offers."""

    def __init__(self, db: Session, weights: MatchingWeights | None = None):
        """Wire repositories and optionally override component weights."""
        self.candidates = CandidateRepository(db)
        self.offers = OfferRepository(db)
        self.weights = (weights or MatchingWeights()).as_dict()

    def score_candidate_for_offer(
        self,
        candidate_id: UUID,
        offer_id: UUID,
    ) -> MatchingScoreResponse | None:
        """Compute matching metrics for a candidate/offer pair."""
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
    ) -> SourcingSearchResponse | None:
        """Rank candidates for a given offer and return a sourcing response."""
        offer = self.offers.get(offer_id)
        if offer is None:
            return None

        candidates = self.candidates.list()
        matches: list[CandidateMatch] = []
        for candidate in candidates:
            score, matched_skills = self._score_candidate(candidate, offer)
            matches.append(
                CandidateMatch(
                    id=candidate.id,
                    name=self._candidate_public_name(candidate),
                    score=round(score, 4),
                    location=self._candidate_location(candidate),
                    skills=matched_skills or self._candidate_skill_names(candidate),
                )
            )

        matches.sort(key=lambda match: match.score, reverse=True)
        return SourcingSearchResponse(candidates=matches[:limit])

    def recommend_offers_for_candidate(
        self,
        candidate_id: UUID,
        limit: int = 10,
    ) -> CandidateRecommendationsResponse | None:
        """Rank offers for a candidate and return a recommendation payload."""
        candidate = self.candidates.get(candidate_id)
        if candidate is None:
            return None

        offers = self.offers.list()
        ranked_offers: list[JobOfferMatch] = []
        for offer in offers:
            score, matched_skills = self._score_candidate(candidate, offer)
            ranked_offers.append(
                JobOfferMatch(
                    offer=offer_to_dto(offer),
                    score=round(score, 4),
                    matched_skills=matched_skills,
                )
            )

        ranked_offers.sort(key=lambda item: item.score, reverse=True)
        return CandidateRecommendationsResponse(offers=ranked_offers[:limit])

    # ------------------------------------------------------------------
    # Component builders
    # ------------------------------------------------------------------
    def _compute_components(self, candidate, offer) -> tuple[dict[str, float], list[str]]:
        """Break down the final matching score into weighted components."""
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
        """Aggregate component scores into a final weighted score."""
        components, matched_skills = self._compute_components(candidate, offer)
        score = sum(self.weights[name] * value for name, value in components.items())
        return score, matched_skills

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize(value: str | None) -> str | None:
        """Normalize raw text for comparisons."""
        if value is None:
            return None
        normalized = value.strip().lower()
        return normalized or None

    def _extract_candidate_skills(self, candidate) -> set[str]:
        """Return normalized skill names from a candidate entity."""
        normalized: set[str] = set()
        for skill in getattr(candidate, "skills", []) or []:
            name = self._normalize(getattr(skill, "name", None))
            if not name:
                continue
            normalized.add(name)
        return normalized

    def _extract_offer_skills(self, offer) -> tuple[set[str], dict[str, str]]:
        """Return normalized offer skills and keep original labels."""
        skill_map: dict[str, str] = {}
        for tag in getattr(offer, "tags", []) or []:
            name = self._normalize(getattr(tag, "nom", None))
            if not name:
                continue
            skill_map[name] = tag.nom.strip()
        return set(skill_map.keys()), skill_map

    # --- coverage & similarity ---
    def _title_similarity(self, candidate, offer) -> float:
        """Score how similar candidate and offer titles/texts are."""
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
        """Gather representative titles from a candidate profile."""
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
        """Tokenize strings into normalized alphanumeric chunks."""
        return re.findall(r"[a-z0-9]+", value.lower())

    # --- geographic fit ---
    def _geo_fit(self, candidate, offer) -> float:
        """Evaluate geographic compatibility between candidate and offer."""
        offer_country = self._normalize(getattr(offer, "work_country_location", None))
        offer_cities = {
            self._normalize(getattr(city, "city", None))
            for city in getattr(offer, "cities", []) or []
        }
        offer_cities.discard(None)

        pref = getattr(candidate, "job_preferences", None)
        cand_country = self._normalize(getattr(pref, "country", None)) or self._normalize(
            getattr(candidate, "country", None)
        )
        # cand_region = self._normalize(getattr(pref, "region", None)) or self._normalize(
        #     getattr(candidate, "region", None)
        # )
        cand_city = self._normalize(getattr(pref, "city", None)) or self._normalize(
            getattr(candidate, "city", None)
        )
        score = 0.0
        if cand_city and cand_city in offer_cities:
            score = 1.0
        elif offer_country and cand_country and offer_country.lower() == cand_country.lower():
            score = 0.5
        
        return score

    # --- seniority / experience ---
    def _seniority_fit(self, candidate, offer) -> float:
        """Compare seniority expectations between the two profiles."""
        candidate_level = self._normalize(getattr(candidate, "experience_level", None))
        offer_level = self._infer_offer_seniority(offer)
        # print(offer)
        if candidate_level and offer_level:
            return 1.0 if candidate_level == offer_level else 0.3
        if candidate_level or offer_level:
            return 0.5
        return 0.4

    def _infer_offer_seniority(self, offer) -> str | None:
        """Guess the seniority level of an offer using tags and text."""
        for tag in getattr(offer, "tags", []) or []:
            normalized = self._normalize(getattr(tag, "name", None))
            if not normalized:
                continue
            mapped = SENIORITY_KEYWORDS.get(normalized)
            if mapped:
                return mapped

        for text in (
            getattr(offer, "title", None),
            getattr(offer, "instructions", None),
        ):
            if not text:
                continue
            for token in self._tokenize(text):
                mapped = SENIORITY_KEYWORDS.get(token)
                if mapped:
                    return mapped
        return None

    # --- languages ---
    def _language_fit(self, candidate, offer) -> float:
        """Compute how well a candidate's languages match offer requirements."""
        candidate_languages = self._candidate_languages(candidate)
        required_languages = self._offer_languages(offer)
        
        if not required_languages:
            return 1.0
        if not candidate_languages:
            return 0.0
        matches = candidate_languages & required_languages
        
        return len(matches) / len(required_languages)

    def _candidate_languages(self, candidate) -> set[str]:
        """Return normalized languages present on the candidate profile."""
        normalized: set[str] = set()
        for language in getattr(candidate, "languages", []) or []:
            name = self._normalize(getattr(language, "language", None))
            if not name:
                continue
            normalized_code = LANGUAGE_ALIASES.get(name, name)
            normalized.add(normalized_code)
        return normalized

    def _offer_languages(self, offer) -> set[str]:
        """Identify languages mentioned on the offer."""
        normalized: set[str] = set()
        for tag in getattr(offer, "tags", []) or []:
            name = self._normalize(getattr(tag, "name", None))
            if not name:
                continue
            code = LANGUAGE_ALIASES.get(name)
            if code:
                normalized.add(code)

        for entry in getattr(offer, "languages", []) or []:
            name = self._normalize(getattr(entry, "language", None))
            if not name:
                continue
            normalized.add(LANGUAGE_ALIASES.get(name, name))

        title = getattr(offer, "title", None)
        instructions = getattr(offer, "instructions", None)
        for text in (title, instructions):
            if not text:
                continue
            for token in self._tokenize(text):
                code = LANGUAGE_ALIASES.get(token)
                if code:
                    normalized.add(code)
        return normalized

    # --- salary fit ---
    def _salary_fit(self, candidate, offer) -> float:
        """Compare salary expectations to offer salary range."""
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
        """Extract a float value from salary expectations."""
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
        """Parse a salary string and return min/max floats."""
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

    # --- candidate helpers for responses ---
    def _candidate_public_name(self, candidate) -> str:
        """Return a display-friendly full name for the candidate."""
        first = (getattr(candidate, "first_name", "") or "").strip()
        last = (getattr(candidate, "last_name", "") or "").strip()
        full_name = f"{first} {last}".strip()
        if full_name:
            return full_name
        fallback = getattr(candidate, "professional_title", None)
        return fallback or "Profil anonyme"

    def _candidate_location(self, candidate) -> str | None:
        """Return the most specific known candidate location."""
        city = getattr(candidate, "city", None)
        region = getattr(candidate, "region", None)
        country = getattr(candidate, "country", None)
        for part in (city, region, country):
            if part:
                return part
        return None

    def _candidate_skill_names(self, candidate) -> list[str]:
        """Return human-readable candidate skill names."""
        names: list[str] = []
        for skill in getattr(candidate, "skills", []) or []:
            title = getattr(skill, "name", None)
            if title:
                names.append(title)
        return names
