from __future__ import annotations

from uuid import UUID
import unicodedata

from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from app.models import Candidate, Offer, OfferSkill
from app.models.enums import Mobility
from app.schemas import SearchBase


class OfferRepository:
    """Data access helper for concrete offers."""

    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return self.db.query(Offer).options(
            selectinload(Offer.skills),
            selectinload(Offer.recruiter),
        )

    def list(self) -> list[Offer]:
        return self._query().all()

    def get(self, offer_id: UUID) -> Offer | None:
        return self._query().filter(Offer.id == offer_id).first()

    def list_by_recruiter(self, recruiter_id: UUID) -> list[Offer]:
        return (
            self._query()
            .filter(Offer.recruiter_id == recruiter_id)
            .all()
        )

    def search_for_candidate(
        self,
        candidate: Candidate,
        search_filters: dict | None = None,
    ) -> list[Offer]:
        filters = search_filters or {}
        query = self._query()

        mobility = filters.get("mobility") or candidate.mobility
        if mobility:
            allowed = {mobility}
            if mobility == Mobility.REMOTE:
                allowed.add(Mobility.HYBRID)
            elif mobility == Mobility.ON_SITE:
                allowed.add(Mobility.HYBRID)
            elif mobility == Mobility.HYBRID:
                allowed.update({Mobility.REMOTE, Mobility.ON_SITE})
            query = query.filter(Offer.mobility.in_(allowed))

        desired_types = (
            [filters.get("contract_type")]
            if filters.get("contract_type")
            else [ptype.type for ptype in candidate.desired_position_types]
        )
        desired_types = [ptype for ptype in desired_types if ptype]
        if desired_types:
            query = query.filter(Offer.position_type.in_(desired_types))

        country = filters.get("country") or candidate.country
        city = filters.get("city") or candidate.city
        if country:
            query = query.filter(Offer.country == country)
        if city:
            query = query.filter(Offer.city == city)

        skill_titles = filters.get("skills") or [skill.title for skill in candidate.skills]
        if skill_titles:
            query = query.filter(Offer.skills.any(OfferSkill.title.in_(skill_titles)))

        return query.all()

    def search_by_payload(self, payload: SearchBase) -> list[Offer]:
        query = self._query()

        if payload.query:
            terms = [
                _normalize_term(term)
                for term in payload.query.split()
                if term.strip()
            ]
            for term in terms:
                like = f"%{term}%"
                query = query.filter(
                    func.lower(
                        func.translate(Offer.title, ACCENTED_CHARS, UNACCENTED_EQUIV)
                    ).like(like)
                    | func.lower(
                        func.translate(Offer.description, ACCENTED_CHARS, UNACCENTED_EQUIV)
                    ).like(like)
                )

        if payload.country:
            query = query.filter(Offer.country == payload.country)
        if payload.city:
            query = query.filter(Offer.city == payload.city)

        if payload.contract_type:
            query = query.filter(Offer.position_type == payload.contract_type)

        return query.all()
ACCENTED_CHARS = "àáâäãåçèéêëìíîïñòóôöõùúûüýÿÀÁÂÄÃÅÇÈÉÊËÌÍÎÏÑÒÓÔÖÕÙÚÛÜÝ"
UNACCENTED_EQUIV = "aaaaaaceeeeiiiinooooouuuuyyAAAAAACEEEEIIIINOOOOOUUUUY"


def _normalize_term(term: str) -> str:
    normalized = unicodedata.normalize("NFKD", term)
    return "".join(c for c in normalized if not unicodedata.combining(c)).lower()
