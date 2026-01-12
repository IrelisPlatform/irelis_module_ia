from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import (
    ContractType,
    DocumentType,
    ExperienceLevel,
    JobOfferStatus,
    JobType,
    LanguageLevel,
    SchoolLevel,
    SkillLevel,
)


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() or "_" for part in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class TagDto(CamelModel):
    name: str | None = None
    type: str | None = None


class RequiredDocumentDto(CamelModel):
    type: DocumentType | None = None


class JobOfferDto(CamelModel):
    id: UUID
    title: str | None = None
    description: str | None = None
    work_country_location: str | None = None
    work_cities: list[str] = Field(default_factory=list)
    contract_type: ContractType | None = None
    status: JobOfferStatus | None = None
    job_type: JobType | None = None
    salary: str | None = None
    published_at: datetime | None = None
    expiration_date: datetime | None = None
    is_featured: bool | None = None
    is_urgent: bool | None = None
    required_languages: list[str] = Field(default_factory=list)
    sector_id: UUID | None = None
    sector_name: str | None = None
    company_name: str | None = None
    company_description: str | None = None
    company_email: str | None = None
    company_length: str | None = None
    company_logo_url: str | None = None
    post_number: int | None = None
    tag_dto: list[TagDto] = Field(default_factory=list)
    required_documents: list[RequiredDocumentDto] = Field(default_factory=list)


class CandidateSkillDto(CamelModel):
    id: UUID
    name: str | None = None
    level: SkillLevel | None = None


class CandidateEducationDto(CamelModel):
    id: UUID
    degree: str | None = None
    institution: str | None = None
    city: str | None = None
    graduation_year: int | None = None


class CandidateLanguageDto(CamelModel):
    id: UUID
    language: str | None = None
    level: LanguageLevel | None = None


class CandidateExperienceDto(CamelModel):
    id: UUID
    position: str | None = None
    company_name: str | None = None
    city: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_current: bool | None = None
    description: str | None = None


class CandidatePreferenceDto(CamelModel):
    desired_position: str | None = None
    contract_types: list[ContractType] = Field(default_factory=list)
    availability: str | None = None
    pretentions_salarial: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    sector_ids: list[UUID] = Field(default_factory=list)
    sectors: list[str] = Field(default_factory=list)


class CandidateDto(CamelModel):
    id: UUID
    professional_title: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    presentation: str | None = None
    email: str | None = None
    phone_number: str | None = None
    school_level: SchoolLevel | None = None
    experience_level: ExperienceLevel | None = None
    avatar_url: str | None = None
    birth_date: datetime | None = None
    linked_in_url: str | None = None
    portfolio_url: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    cv_url: str | None = None
    motivation_letter_url: str | None = None
    pitch_mail: str | None = None
    skills: list[CandidateSkillDto] = Field(default_factory=list)
    educations: list[CandidateEducationDto] = Field(default_factory=list)
    languages: list[CandidateLanguageDto] = Field(default_factory=list)
    experiences: list[CandidateExperienceDto] = Field(default_factory=list)
    preference: CandidatePreferenceDto | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
