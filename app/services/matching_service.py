from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from uuid import UUID
from fastapi import HTTPException

from sqlalchemy.orm import Session

import json


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
from app.utils.offer_management import extract_text_from_rich_json
from app.utils.cache import APP_CACHE, make_cache_key


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
    geo_fit: float = 0.25
    seniority: float = 0.10
    language: float = 0.10
    salary: float = 0.00
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
        self.stop_words = {
            "le", "la", "les", "un", "une", "des", "et", "ou", "de", "du", "en", "au", "aux", 
            "ce", "cette", "pour", "par", "dans", "sur", "avec", "sans", "est", "sont", "a", 
            "the", "and", "of", "to", "in", "on", "with", "for", "is", "are", "it", "that", "this"
        }
        # Define weights
        self.weights = {
            "coverage": 0.30,
            "title_similarity": 0.20,
            "geo_fit": 0.15,
            "seniority": 0.10,
            "language": 0.10,
            "salary": 0.10,
            "profile_focus": 0.05
        } 

    def matching_cv_job_offer(self, job_offer_id: UUID, content: str):
        """Compute matching metrics for a cv/offer pair."""
        
        # Assuming self.offers is a repository/service that returns a JobOffer Object
        offer = self.offers.get(job_offer_id) 
        
        if offer is None:
            return None
        
        score, matched_skills = self._score_cv(content, offer)
        
        # Return simple dict or your specific MatchingScoreResponse object
        return {
            "score": round(score, 4),
            "matched_skills": ["not yet"]
        }
    
    def _score_cv(self, content, offer) -> tuple[float, list[str]]:
        """Aggregate component scores into a final weighted score."""
        components, matched_skills = self._compute_components2(content, offer)
        
        # Calculate weighted sum
        score = sum(self.weights[name] * value for name, value in components.items())
        
        # Normalize to 0-100 scale
        final_percentage = min(max(score, 0.0), 1.0) * 100
        
        return round(final_percentage, 2), matched_skills
    
    def _compute_components2(self, content: str, offer) -> tuple[dict[str, float], list[str]]:
        """Break down the final matching score into weighted components."""
        # 1. Prepare Data
        cv_text_norm = self._normalize_text2(content)
        cv_tokens = set(cv_text_norm.split())
        
        # Extract skills/keywords from Offer Description
        description = getattr(offer, "description", "")
        # description =  """{\"root\":{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"L'ACMS recherche des candidats (HiF) hautement qualifiés pour mener les missions de\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Data Analyst dans le cadre d'un projet.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Qui recrutons nous ?\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Le Data Analyst sera responsable de I'extraction, le nettoyage et I'analyse des données\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"du projet.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Missions essentielles\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Extraire et nettoyer des données à partir de sources variées (bases\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"internationales DHS, MICS, rapports de subventions, bases administratives) ; . Effectuer des analyses statistiques descriptives et inférentielles sur des données de santé ; . Préparer des jeux de données pour analyse (data wrangling, transformation) ; . Contribuer à la production de rapports d'analyse et de synthèses de données ; .\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Assister le Senior Data Scientist dans le développement de modèles\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"statistiques ; . Documenter les processus d'extraction et d'analyse pour garantir la\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"reproductibilité ; . Participer au contrôle qualité des données.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Qualifications et compétences requises :\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Être titulaire d'un Maitrise/Master en statistiques, biostatistiques, data science,\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"économétrie ou domaine connexe ; (8 points)\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Avoir au moins 3 ans d'expérience dans l'analyse des données (idéalement dans\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"le secteur de la santé) ; (8 Points)\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Maîtrise avancée de R eUou Python pour J'analyse de données (8 points) ; . Bonne connaissance de STATA, SPSS ou SAS (8 points) ;\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Références et autres compétences souhaitées : . Expérience en manipulation de grandes bases de données (data cleaning, data wrangling) ; . Connaissance des enquêtes DHS, tUICS ou autres bases de données sanitaires\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"internationales ; . Capacité à produire des visualisations claires (ggplot2, matplotlib, etc.) ; o Expérience de travail avec des données de programmes de santé en Afrique est\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"un atout ; . Parler couramment le français et avoir une connaissance pratique de J'anglais.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Comment constituer votre Dossier de candidature ?\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":9,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Le dossier doit comporter : .\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\" Une lettre de motivation (une page maximum).\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Un Curriculum Vitae avec les noms et adresses de trois références. Une\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"vérification des références sera effectuée pour le candidat retenu.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Une photocopie d'une pièce d'identification valide.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Une photocopie du diplôme requis.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Les justificatifs des expériences professionnelles.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Clause relative aux candidatures des fonctionnaires\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Le fonctionnaire qui collabore avec I'ACMS dans le cadre de cette mission devra\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"fournir la preuve de son désengagement avec son administration d'origine avant\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"la signature de son contrat.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Toute information erronée, falsifiée ou dissimulée, découverte au cours du\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"processus de recrutement ou après l'embauche, entraînera la rupture immédiate\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"du contrat, sans préjudice des autres mesures administratives applicables.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Les dossiers complets doivent être envoyés uniquement par email à l'adresse suivante\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\": CM_recrutement@acms-cmr.org\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Aucune candidature physique ne sera acceptée.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Politique RH de I'AGMS\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". Seuls les candidats présélectionnés seront contactés\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\". L'ACIVS garantit l'égalité des chances et encourage vivement les candidatures\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"féminines.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"informations clés sur la mission : . Type de contrat : Consultation\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"o Date de début de mission souhaitée . Avril 2026\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"root\",\"version\":1}}""""
        
        offer_desc_text = self._parse_rich_description2(description)
        offer_skills = self._extract_keywords2(offer_desc_text)
        
        # 2. Calculate Overlap
        overlap = offer_skills.intersection(cv_tokens)
        matched_skills = list(overlap)

        # 3. Calculate Metrics
        coverage = len(overlap) / len(offer_skills) if offer_skills else 0.0
        
        # Profile Focus: (Keywords matched / Total unique words in CV)
        profile_focus = len(overlap) / len(cv_tokens) if cv_tokens else 0.0

        components = {
            "coverage": coverage,
            "title_similarity": self._title_similarity2(content, offer),
            "geo_fit": self._geo_fit2(content, offer),
            "seniority": self._seniority_fit2(content, offer),
            "language": self._language_fit2(content, offer),
            "salary": self._salary_fit2(content, offer),
            "profile_focus": profile_focus,
        }

        return components, matched_skills
        
    def _title_similarity2(self, content: str, offer) -> float:
        """Check if words from the Job Title appear in the CV."""
        title = getattr(offer, "title", "")
        if not title: 
            return 0.0
        
        title_keywords = self._extract_keywords2(title)
        # cv_keywords = self._extract_keywords2(content)
        
        if not title_keywords:
            return 0.0

        result = sum(1 for word in title_keywords if word in content) / len(title_keywords)
        
        return result

    def _geo_fit2(self, content: str, offer) -> float:
        """Check if Country or City is mentioned in the CV."""
        locations = []
        
        # FIXED: Handle list of objects for cities
        cities = getattr(offer, "cities", [])
        for city_obj in cities:
            city_name = city_obj.get("city") if isinstance(city_obj, dict) else getattr(city_obj, "city", "")
            locations.append(city_name)
        
        content_norm = self._normalize_text2(content)
        
        for loc in locations:
            print(content_norm)
            if loc and self._normalize_text2(loc) in content_norm:
                return 1.0
        
        return 0.0

    def _seniority_fit2(self, content: str, offer) -> float:
        """Check for years patterns in offer description vs CV."""
       
        description = getattr(offer, "description", "")
        desc_text = self._parse_rich_description2(description)
        required_years = re.findall(r"(\d+)\s*(?:an|ans|year|years)", desc_text, re.IGNORECASE)
        
        if not required_years:
            return 1.0 
            
        max_required = max([int(y) for y in required_years])
        
        # Look for years in CV
        cv_years = re.findall(r"(\d+)\s*(?:an|ans|year|years)", content, re.IGNORECASE)
        if not cv_years:
            return 0.0
            
        max_cv = max([int(y) for y in cv_years])
        
        if max_cv >= max_required:
            return 1.0
        else:
            return max_cv / max_required

    def _language_fit2(self, content: str, offer) -> float:
        """Check if required languages are in CV."""
        # FIXED: Handle list of objects for languages
        languages = getattr(offer, "languages", [])
        required_langs = []
        
        for l in languages:
             # Check if l is a dict or an object
            lang_name = l.get("language") if isinstance(l, dict) else getattr(l, "language", "")
            required_langs.append(lang_name)
        
        if not required_langs:
            return 1.0
            
        content_norm = self._normalize_text2(content)
        matches = 0
        for lang in required_langs:
            if lang and self._normalize_text2(lang) in content_norm:
                matches += 1
                
        return matches / len(required_langs)

    def _salary_fit2(self, content: str, offer) -> float:
        """Neutral score if salary is missing."""
        
        salary = getattr(offer, "salary", None)
        if not salary:
            return 1.0
        return 0.5 

    # --- 3. HELPER UTILS ---

    def _normalize_text2(self, text: str) -> str:
        if not text: return ""
        text = text.lower()
        return re.sub(r'[^\w\s]', '', text)

    def _extract_keywords2(self, text: str) -> set[str]:
        tokens = self._normalize_text2(text).split()
        return {word for word in tokens if word not in self.stop_words and len(word) > 2}

    def _parse_rich_description2(self, json_desc_str: str) -> str:
        if not json_desc_str: return ""
        try:
            # Check if it's actually JSON
            if not isinstance(json_desc_str, str) or not json_desc_str.strip().startswith("{"):
                return str(json_desc_str)
                
            data = json.loads(json_desc_str)
            root = data.get("root", {})
            
            def recurse(node):
                text = ""
                if "text" in node: text += node["text"] + " "
                if "children" in node:
                    for child in node["children"]:
                        text += recurse(child)
                return text
                
            return recurse(root)
        except:
            return str(json_desc_str)

    #?========================================================================================================
    #? HERE IS just for a simple score
    #?========================================================================================================

    def score_candidate_for_offer(
        self,
        candidate_id: UUID,
        offer_id: UUID,
    ) :
        #-> MatchingScoreResponse | None
        """Compute matching metrics for a candidate/offer pair."""
        candidate = self.candidates.get(candidate_id)
        offer = self.offers.get(offer_id)
        
        if candidate is None or offer is None:
            return None
        score, matched_skills = self._score_candidate(candidate, offer)
        response = MatchingScoreResponse(score=round(score, 4), matched_skills=matched_skills)
        # APP_CACHE.set(cache_key, response)
        return response
    
    
    def rank_candidates_for_offer(
        self,
        offer_id: UUID,
        limit: int = 10,
    ) -> SourcingSearchResponse | None:
        """Rank candidates for a given offer and return a sourcing response."""
        # cache_key = make_cache_key("matching:rank_candidates", offer_id, limit=limit)
        # found, cached = APP_CACHE.get(cache_key)
        # if found:
        #     return cached
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
        response = SourcingSearchResponse(candidates=matches[:limit])
        # APP_CACHE.set(cache_key, response)
        return response

    def recommend_offers_for_candidate(
        self,
        candidate_id: UUID,
        limit: int = 10,
    ) -> CandidateRecommendationsResponse | None:
        """Rank offers for a candidate and return a recommendation payload."""
        # cache_key = make_cache_key("matching:recommend_offers", candidate_id, limit=limit)
        # found, cached = APP_CACHE.get(cache_key)
        # if found:
        #     return cached
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
        response = CandidateRecommendationsResponse(offers=ranked_offers[:limit])
        # APP_CACHE.set(cache_key, response)
        return response

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
