from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import SearchTarget, SearchType
from app.repositories.search_repository import SearchRepository
from app.repositories.user_repository import UserRepository
from app.schemas import JobOfferDto, SearchCreate
from app.services.dto_mappers import offer_to_dto
from app.utils.cache import APP_CACHE, make_cache_key
from app.utils.search_filters import as_list


class SearchService:
    """Business logic dedicated to search workflows."""

    def __init__(self, db: Session):
        """Initialize repositories used for search workflows."""
        self.repo = SearchRepository(db)
        self.user_repo = UserRepository(db)

    def search_by_payload(self, payload: SearchCreate) -> list[JobOfferDto]:
        """Search offers with explicit payload filters."""
        cache_key = make_cache_key("search:payload", payload)
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached
        offers = [offer_to_dto(offer) for offer in self.repo.search_by_payload(payload)]
        APP_CACHE.set(cache_key, offers)
        return offers


    def search_for_candidate_by_user(
        self,
        user_id: UUID,
        payload: SearchCreate | None = None,
    ) -> list[JobOfferDto] | None:
        """Search offers for a given user, enriching filters with candidate data."""
        candidate = self.user_repo.get_candidate_by_user_id(user_id)
        
        if candidate is None:
            user = self.user_repo.get(user_id)
            if user is None: 
                return None
            else:
                cache_key = make_cache_key("search:by_user", user_id, payload=payload)
                found, cached = APP_CACHE.get(cache_key)
                if found:
                    self.repo.record_search(user_id, payload)
                    return cached
                offers = [offer_to_dto(offer) for offer in self.repo.search_by_payload(payload)]
                self.repo.record_search(user_id, payload)
                APP_CACHE.set(cache_key, offers)
                return offers

        filters = payload.model_dump(exclude_none=True) if payload else None
        cache_key = make_cache_key("search:by_candidate", user_id, filters=filters)
        found, cached = APP_CACHE.get(cache_key)
        if found:
            self.repo.record_search(user_id, payload)
            return cached
        offers = [offer_to_dto(offer) for offer in self.repo.search_for_candidate(candidate, filters)]
        self.repo.record_search(user_id, payload)
        APP_CACHE.set(cache_key, offers)
        return offers

    def recommend_offers_from_search_history(
        self,
        user_id: UUID,
        history_limit: int = 5,
    ) -> list[JobOfferDto] | None:
        """Recommend offers using the user's recent search history."""
        user = self.user_repo.get(user_id)
        if user is None:
            return None

        searches = self.repo.list_recent_searches_by_user(user_id, history_limit)
        if not searches:
            return []

        search_ids = [search.id for search in searches]
        cache_key = make_cache_key(
            "recommendations:search_history",
            user_id,
            history_limit,
            search_ids,
        )
        found, cached = APP_CACHE.get(cache_key)
        if found:
            return cached

        payload = self._build_payload_from_history(searches)
        offers = [offer_to_dto(offer) for offer in self.repo.search_by_payload(payload)]
        APP_CACHE.set(cache_key, offers)
        return offers

    def _build_payload_from_history(self, searches) -> SearchCreate:
        """Build a search payload from recent search entries."""
        query_terms: list[str] = []
        seen_terms: set[str] = set()

        def _add_query_terms(query: str) -> None:
            for term in query.split():
                cleaned = term.strip()
                if not cleaned:
                    continue
                normalized = cleaned.lower()
                if normalized in seen_terms:
                    continue
                seen_terms.add(normalized)
                query_terms.append(cleaned)

        for search in searches:
            if search.query:
                _add_query_terms(search.query)

        def _pick(field_name: str):
            for search in searches:
                value = getattr(search, field_name)
                if value:
                    return value
            return None

        contract_type_value = _pick("type_contrat")
        contract_types = as_list(contract_type_value) if contract_type_value else None
        if contract_types == []:
            contract_types = None

        query = " ".join(query_terms) if query_terms else None
        return SearchCreate(
            query=query,
            type=SearchType.BOOL,
            target=SearchTarget.OFFRE,
            country=_pick("country"),
            city=_pick("city"),
            town=_pick("town"),
            contract_type=contract_types,
            language=_pick("language"),
            date_publication=_pick("date_publication"),
        )
