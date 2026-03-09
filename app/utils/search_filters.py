from __future__ import annotations

from datetime import datetime
from typing import Iterable
from unidecode import unidecode

from sqlalchemy import or_, func

from app.models import JobOffer, Tag


def normalize(value: str | None) -> str | None:
    """Lowercase, trim and remove accents from incoming text."""
    if value is None:
        return None
    # Supprime les accents et les caractères spéciaux
    normalized = unidecode(value).strip().lower()
    return normalized or None


def as_list(value) -> list:
    """Coerce search parameters into a list."""
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return [item for item in value if item]
    return [value]


def parse_datetime(value):
    """Parse acceptable datetime inputs to datetime objects."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def enum_to_str(value) -> str | None:
    """Return the string value for enums."""
    if value is None:
        return None
    return value.value if hasattr(value, "value") else str(value)


def list_to_csv(value) -> str | None:
    """Serialize list-like values into a comma-separated string."""
    items = [item for item in as_list(value) if item is not None]
    normalized = [enum_to_str(item) for item in items if enum_to_str(item)]
    return ", ".join(normalized) if normalized else None


def apply_text_search(query, raw_terms):
    """Apply LIKE-based search over multiple offer fields."""
    if not raw_terms:
        return query

    if isinstance(raw_terms, str):
        terms = [term.strip() for term in raw_terms.split() if term.strip()]
    elif isinstance(raw_terms, Iterable):
        terms: list[str] = []
        for part in raw_terms:
            if not part:
                continue
            terms.extend([sub.strip() for sub in str(part).split() if sub.strip()])
    else:
        value = str(raw_terms).strip()
        terms = [value] if value else []

    if not terms:
        return query

    search_clauses = []
    for term in terms:
        normalized_term = normalize(term)
        if not normalized_term:
            continue
        like_term = f"%{normalized_term}%"
        search_clauses.append(
            or_(
                func.lower(func.unaccent(JobOffer.title)).like(like_term),
                JobOffer.tags.any(func.lower(func.unaccent(Tag.name)).like(like_term)),
            )
        )

    return query.filter(or_(*search_clauses))
