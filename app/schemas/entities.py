from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import (
    ApplicationStatus,
    ContractType,
    DocumentType,
    ExperienceLevel,
    JobOfferStatus,
    JobType,
    LanguageLevel,
    OtpPurpose,
    Provider,
    SchoolLevel,
    SkillLevel,
    UserRole,
    UserType,
    SearchTarget,
    SearchType,
)


class UserBase(BaseModel):
    email: EmailStr
    role: str
    provider: str
    user_type: str | None = None


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    deleted: bool
    deleted_at: datetime | None = None
    email_verified_at: datetime | None = None
    # last_login n'est pas dans la table users du dump, donc retiré

    class Config:
        from_attributes = True


class SectorRead(BaseModel):
    id: UUID
    name: str | None = None
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class TagRead(BaseModel):
    id: UUID
    name: str
    type: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class SearchRead(BaseModel):
    id: UUID
    query: str
    type: SearchType
    target: SearchTarget
    country: str | None = None
    city: str | None = None
    town: str | None = None
    type_contrat: str | None = None
    niveau_etude: str | None = None
    experience: str | None = None
    language: str | None = None
    date_publication: datetime | None = None
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SearchBase(BaseModel):
    query: str | None = None
    type: SearchType | None = None
    target: SearchTarget | None = None
    country: str | None = None
    city: str | None = None
    town: str | None = None
    type_contrat: ContractType | list[ContractType] | None = None
    contract_type: ContractType | list[ContractType] | None = None
    niveau_etude: SchoolLevel | None = None
    school_level: SchoolLevel | None = None
    experience: ExperienceLevel | None = None
    experience_level: ExperienceLevel | None = None
    language: str | None = None
    date_publication: datetime | None = None
    skills: list[str] | None = None


class SearchCreate(SearchBase):
    user_id: UUID | None = None


class MatchingScoreRequest(BaseModel):
    candidate_id: UUID
    offer_id: UUID


class MatchingScoreResponse(BaseModel):
    score: float
    matched_skills: list[str] = Field(default_factory=list)


class CandidateMatch(BaseModel):
    id: UUID
    name: str
    score: float
    location: str | None = None
    skills: list[str] = Field(default_factory=list)


class SourcingSearchResponse(BaseModel):
    candidates: list[CandidateMatch] = Field(default_factory=list)


class EducationRead(BaseModel):
    id: UUID
    city: str | None = None
    degree: str | None = None
    graduation_year: int | None = None
    institution: str | None = None
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ExperienceRead(BaseModel):
    id: UUID
    city: str | None = None
    company_name: str | None = None
    description: str | None = None
    end_date: datetime | None = None
    is_current: bool | None = None
    position: str | None = None
    start_date: datetime
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class SkillRead(BaseModel):
    id: UUID
    level: SkillLevel | None = None
    name: str | None = None
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class LanguageRead(BaseModel):
    id: UUID
    language: str | None = None
    level: LanguageLevel | None = None
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class JobPreferencesContractTypeRead(BaseModel):
    contract_type: ContractType

    class Config:
        from_attributes = True


class JobPreferencesSectorLinkRead(BaseModel):
    sector_id: UUID
    sector: SectorRead | None = None

    class Config:
        from_attributes = True


class JobPreferencesRead(BaseModel):
    id: UUID
    availability: str | None = None
    desired_position: str | None = None
    city: str | None = None
    country: str | None = None
    region: str | None = None
    pretentions_salarial: str | None = None
    candidate_id: UUID
    contract_types: list[JobPreferencesContractTypeRead] = Field(default_factory=list)
    sectors: list[JobPreferencesSectorLinkRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ApplicationDocumentRead(BaseModel):
    id: UUID
    application_id: UUID | None = None
    storage_url: str | None = None
    type: DocumentType | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ApplicationRead(BaseModel):
    id: UUID
    message: str | None = None
    status: ApplicationStatus | None = None
    candidate_id: UUID
    job_offer_id: UUID
    applied_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None
    documents: list[ApplicationDocumentRead] = Field(default_factory=list)

    class Config:
        from_attributes = True


class SavedJobOfferRead(BaseModel):
    id: UUID
    candidate_id: UUID
    job_offer_id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class CandidateRead(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    avatar_url: str | None = None
    birth_date: datetime | None = None
    completion_rate: float | None = None
    cv_url: str | None = None
    experience_level: str | None = None
    first_name: str | None = None
    is_visible: bool | None = None
    last_viewed_month: date | None = None
    monthly_profile_views: int | None = None
    profile_views: int | None = None
    last_name: str | None = None
    linked_in_url: str | None = None
    city: str | None = None
    country: str | None = None
    region: str | None = None
    motivation_letter_url: str | None = None
    phone_number: str | None = None
    pitch_mail: str | None = None
    portfolio_url: str | None = None
    presentation: str | None = None
    professional_title: str | None = None
    school_level: str | None = None
    user_id: UUID | None = None
    job_preferences: JobPreferencesRead | None = None
    educations: list[EducationRead] = Field(default_factory=list)
    experiences: list[ExperienceRead] = Field(default_factory=list)
    skills: list[SkillRead] = Field(default_factory=list)
    languages: list[LanguageRead] = Field(default_factory=list)
    applications: list[ApplicationRead] = Field(default_factory=list)
    saved_job_offers: list[SavedJobOfferRead] = Field(default_factory=list)

    class Config:
        from_attributes = True


class RecruiterRead(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    company_description: str | None = None
    company_email: str | None = None
    company_length: int | None = None
    company_linked_in_url: str | None = None
    company_logo_url: str | None = None
    company_name: str | None = None
    company_phone: str | None = None
    company_website: str | None = None
    first_name: str | None = None
    function: str | None = None
    last_name: str | None = None
    city: str | None = None
    country: str | None = None
    region: str | None = None
    phone_number: str | None = None
    sector_id: UUID | None = None
    user_id: UUID | None = None
    sector: SectorRead | None = None

    class Config:
        from_attributes = True


class JobOfferBase(BaseModel):
    contract_type: ContractType | None = None
    description: str | None = None
    expiration_date: datetime | None = None
    instructions: str | None = None
    is_featured: bool | None = None
    is_urgent: bool | None = None
    job_type: JobType | None = None
    post_number: int | None = None
    salary: str | None = None
    published_at: datetime | None = None
    required_language: str | None = None
    status: JobOfferStatus | None = None
    title: str | None = None
    work_city_location: str | None = None
    work_country_location: str | None = None
    benefits: int | None = None
    requirements: int | None = None
    responsibilities: int | None = None


class CandidatureInfoRead(BaseModel):
    id: UUID
    job_offer_id: UUID
    email_candidature: str | None = None
    instructions: str | None = None
    required_documents: str | None = None
    url_candidature: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class RequiredDocumentRead(BaseModel):
    id: UUID
    job_offer_id: UUID | None = None
    type: DocumentType | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class JobOfferRead(JobOfferBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    recruiter: RecruiterRead | None = None
    applications: list[ApplicationRead] = Field(default_factory=list)
    tags: list[TagRead] = Field(default_factory=list)
    candidature_info: CandidatureInfoRead | None = None
    required_documents: list[RequiredDocumentRead] = Field(default_factory=list)

    class Config:
        from_attributes = True


class EmailOtpRead(BaseModel):
    id: int
    code: str
    consumed: bool
    email: EmailStr
    expires_at: datetime
    purpose: OtpPurpose
    user_type: UserType | None = None

    class Config:
        from_attributes = True


class UserSessionRead(BaseModel):
    id: UUID
    device_info: str | None = None
    expired_at: datetime | None = None
    ip_address: str | None = None
    is_active: bool | None = None
    token: str | None = None
    user_id: UUID | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
