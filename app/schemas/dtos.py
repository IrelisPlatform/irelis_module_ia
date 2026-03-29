from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

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

class RequiredDocumentDto(CamelModel):
    type: DocumentType | None = None

class TagDto(CamelModel):
    name: str | None = None
    type: str | None = None


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
    

#! ======================================================================
#! Chat management
#! ======================================================================

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    receiver_id: UUID
    sender_id: UUID

class MessageResponse(MessageBase):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    created_at: datetime
    is_read: bool
    model_config = ConfigDict(from_attributes=True)

# --- Inbox ---
class ConversationSummary(BaseModel):
    partner_id: UUID
    partner_name: str  # Add Email or Name of the partner 
    last_message: str
    last_message_at: datetime
    unread_count: int

# --- Blocage ---
class BlockCreate(BaseModel):
    user_id_to_block: UUID

class BlockResponse(BaseModel):
    message: str
    is_blocked: bool
    
# Le nouveau schéma pour forcer Gemini à renvoyer un tableau
class JobOfferList(BaseModel):
    offers: list[JobOfferDto]

# Le schéma pour la requête de ton endpoint
class ScrapeRequest(BaseModel):
    url: HttpUrl


class ScoreBreakdown(BaseModel):
    skills_score: int = Field(description="Score sur 100 pour les compétences techniques et soft skills")
    experience_score: int = Field(description="Score sur 100 pour la séniorité et les années d'expérience pertinentes")
    geo_score: int = Field(description="Score sur 100 pour la localisation (100 si le candidat est dans le pays/ville, sinon moins)")
    language_score: int = Field(description="Score sur 100 pour la maîtrise des langues exigées")

class MatchingScoreResponse(BaseModel):
    score: int = Field(description="Score de compatibilité global sur 100 (pondération logique des sous-scores)")
    breakdown: ScoreBreakdown
    matched_skills: list[str] = Field(description="Compétences clés de l'offre trouvées dans le CV")
    missing_skills: list[str] = Field(description="Compétences exigées par l'offre MAIS absentes du CV")
    justification: str = Field(description="Un paragraphe court (3-4 phrases) justifiant le score, destiné au recruteur.") 