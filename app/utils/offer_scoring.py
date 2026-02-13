from __future__ import annotations

from typing import Iterable

from app.schemas import JobOfferDto, SearchCreate
from app.utils.search_filters import enum_to_str, normalize


_COUNTRY_WEIGHT = 0.2
_CITY_WEIGHT = 0.4
_LANGUAGE_WEIGHT = 0.3
_CONTRACT_WEIGHT = 0.2
_DATE_WEIGHT = 0.1

def rank_offers_by_search(
    offers: list[JobOfferDto],
    payload: SearchCreate | None,
) -> list[JobOfferDto]:
    """Return offers ordered by descending score for the provided search payload."""
    if not offers or payload is None:
        return offers

    scored = [(offer, _score_offer(payload, offer)) for offer in offers]
    scored.sort(key=lambda item: item[1], reverse=True)
    return [offer for offer, _ in scored]


def _score_offer(payload: SearchCreate, offer: JobOfferDto) -> float:
    """Compute a weighted similarity score between the search payload and offer."""
    score = 0.0

    #? if _matches_country(payload.country, offer):
    #?     score += _COUNTRY_WEIGHT
    if _matches_city(payload, offer):
        score += _CITY_WEIGHT
    if _matches_contract_type(payload.contract_type, offer):
        score += _CONTRACT_WEIGHT
    if _matches_language(payload.language, offer):
        score += _LANGUAGE_WEIGHT
    if _matches_date(payload.date_publication, offer):
        score += _DATE_WEIGHT

    return round(score, 6)


def _matches_country(country: str | None, offer: JobOfferDto) -> bool:
    if not country:
        return False
    country_norm = normalize(country)
    offer_country = normalize(offer.work_country_location)
    return bool(country_norm and offer_country and country_norm == offer_country)


def _matches_city(payload: SearchCreate, offer: JobOfferDto) -> bool:
    city = payload.city or payload.town
    if not city:
        return False
    city_norm = normalize(city)
    if not city_norm:
        return False
    
    for value in offer.cities:
        if normalize(value.city) == city_norm:
            return True
    return False


def _matches_contract_type(contract_type, offer: JobOfferDto) -> bool:
    if contract_type is None:
        return False
    offer_value = enum_to_str(offer.contract_type)
    if not offer_value:
        return False
    if isinstance(contract_type, Iterable) and not isinstance(contract_type, (str, bytes)):
        allowed = {enum_to_str(item) for item in contract_type if enum_to_str(item)}
        return offer_value in allowed
    return offer_value == enum_to_str(contract_type)


def _matches_language(language: str | None, offer: JobOfferDto) -> bool:
    if not language:
        return False
    lang_norm = normalize(language)
    if not lang_norm:
        return False
    for value in offer.required_languages:
        if normalize(value) == lang_norm:
            return True
    return False


def _matches_date(date_publication, offer: JobOfferDto) -> bool:
    if date_publication is None or offer.published_at is None:
        return False
    return offer.published_at >= date_publication
