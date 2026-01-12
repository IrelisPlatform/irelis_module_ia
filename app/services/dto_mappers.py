from __future__ import annotations

from app.models import Candidate, JobOffer
from app.schemas.dtos import (
    CandidateDto,
    CandidateEducationDto,
    CandidateExperienceDto,
    CandidateLanguageDto,
    CandidatePreferenceDto,
    CandidateSkillDto,
    JobOfferDto,
    RequiredDocumentDto,
    TagDto,
)


def _as_text(value) -> str | None:
    if value is None:
        return None
    return str(value)


def offer_to_dto(offer: JobOffer) -> JobOfferDto:
    recruiter = getattr(offer, "recruiter", None)
    sector = getattr(recruiter, "sector", None) if recruiter else None

    return JobOfferDto(
        id=offer.id,
        title=getattr(offer, "title", None),
        description=_as_text(getattr(offer, "description", None)),
        work_country_location=getattr(offer, "work_country_location", None),
        work_cities=[
            city.city
            for city in (getattr(offer, "cities", []) or [])
            if city.city
        ],
        contract_type=getattr(offer, "contract_type", None),
        status=getattr(offer, "status", None),
        job_type=getattr(offer, "job_type", None),
        salary=getattr(offer, "salary", None),
        published_at=getattr(offer, "published_at", None),
        expiration_date=getattr(offer, "expiration_date", None),
        is_featured=getattr(offer, "is_featured", None),
        is_urgent=getattr(offer, "is_urgent", None),
        required_languages=[
            language.language
            for language in (getattr(offer, "languages", []) or [])
            if language.language
        ],
        sector_id=getattr(sector, "id", None) if sector else None,
        sector_name=getattr(sector, "name", None) if sector else None,
        company_name=getattr(recruiter, "company_name", None) if recruiter else None,
        company_description=_as_text(getattr(recruiter, "company_description", None))
        if recruiter
        else None,
        company_email=getattr(recruiter, "company_email", None) if recruiter else None,
        company_length=getattr(recruiter, "company_length", None) if recruiter else None,
        company_logo_url=getattr(recruiter, "company_logo_url", None)
        if recruiter
        else None,
        post_number=getattr(offer, "post_number", None),
        tag_dto=[
            TagDto(name=tag.name, type=tag.type)
            for tag in (getattr(offer, "tags", []) or [])
            if tag.name or tag.type
        ],
        required_documents=[
            RequiredDocumentDto(type=doc.type)
            for doc in (getattr(offer, "required_documents", []) or [])
            if doc.type
        ],
    )


def candidate_to_dto(candidate: Candidate) -> CandidateDto:
    user = getattr(candidate, "user", None)
    preference = getattr(candidate, "job_preferences", None)

    preference_dto = None
    if preference:
        contract_types = [
            pref.contract_type
            for pref in (getattr(preference, "contract_types", []) or [])
            if pref.contract_type
        ]
        sector_links = getattr(preference, "sectors", []) or []
        sector_ids = [link.sector_id for link in sector_links if link.sector_id]
        sectors = [
            link.sector.name
            for link in sector_links
            if link.sector and link.sector.name
        ]
        preference_dto = CandidatePreferenceDto(
            desired_position=getattr(preference, "desired_position", None),
            contract_types=contract_types,
            availability=getattr(preference, "availability", None),
            pretentions_salarial=getattr(preference, "pretentions_salarial", None),
            country=getattr(preference, "country", None),
            region=getattr(preference, "region", None),
            city=getattr(preference, "city", None),
            sector_ids=sector_ids,
            sectors=sectors,
        )

    return CandidateDto(
        id=candidate.id,
        professional_title=getattr(candidate, "professional_title", None),
        first_name=getattr(candidate, "first_name", None),
        last_name=getattr(candidate, "last_name", None),
        presentation=getattr(candidate, "presentation", None),
        email=getattr(user, "email", None) if user else None,
        phone_number=getattr(candidate, "phone_number", None),
        school_level=getattr(candidate, "school_level", None),
        experience_level=getattr(candidate, "experience_level", None),
        avatar_url=getattr(candidate, "avatar_url", None),
        birth_date=getattr(candidate, "birth_date", None),
        linked_in_url=getattr(candidate, "linked_in_url", None),
        portfolio_url=getattr(candidate, "portfolio_url", None),
        country=getattr(candidate, "country", None),
        region=getattr(candidate, "region", None),
        city=getattr(candidate, "city", None),
        cv_url=getattr(candidate, "cv_url", None),
        motivation_letter_url=getattr(candidate, "motivation_letter_url", None),
        pitch_mail=getattr(candidate, "pitch_mail", None),
        skills=[
            CandidateSkillDto(id=skill.id, name=skill.name, level=skill.level)
            for skill in (getattr(candidate, "skills", []) or [])
        ],
        educations=[
            CandidateEducationDto(
                id=edu.id,
                degree=edu.degree,
                institution=edu.institution,
                city=edu.city,
                graduation_year=edu.graduation_year,
            )
            for edu in (getattr(candidate, "educations", []) or [])
        ],
        languages=[
            CandidateLanguageDto(
                id=lang.id, language=lang.language, level=lang.level
            )
            for lang in (getattr(candidate, "languages", []) or [])
        ],
        experiences=[
            CandidateExperienceDto(
                id=exp.id,
                position=exp.position,
                company_name=exp.company_name,
                city=exp.city,
                start_date=exp.start_date,
                end_date=exp.end_date,
                is_current=exp.is_current,
                description=exp.description,
            )
            for exp in (getattr(candidate, "experiences", []) or [])
        ],
        preference=preference_dto,
        created_at=getattr(candidate, "created_at", None),
        updated_at=getattr(candidate, "updated_at", None),
    )
