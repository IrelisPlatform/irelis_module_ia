from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.enums import (
    LanguageLevel,
    Mobility,
    NotificationDelay,
    PositionType,
    RecommendationTarget,
    SalaryType,
    SearchTarget,
    SearchType,
    SeniorityLevel,
    UserRole,
)


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    role: UserRole = UserRole.CANDIDATE


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class CandidateBase(BaseModel):
    mobility: Mobility | None = None
    country: str | None = None
    city: str | None = None
    town: str | None = None
    address: str | None = None
    salary_min: Decimal | None = None
    salary_avg: Decimal | None = None
    salary_max: Decimal | None = None
    notification_delay: NotificationDelay | None = None
    notification_enabled: bool = True


class CandidateCreate(CandidateBase):
    user_id: UUID


class CandidateRead(CandidateBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class RecruiterBase(BaseModel):
    organization_name: str


class RecruiterCreate(RecruiterBase):
    user_id: UUID


class RecruiterRead(RecruiterBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationBase(BaseModel):
    label: str
    target: RecommendationTarget


class RecommendationCreate(RecommendationBase):
    user_id: UUID
    number: int = 0


class RecommendationRead(RecommendationBase):
    id: UUID
    user_id: UUID
    number: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    token: str
    bot: bool = False


class ChatSessionCreate(ChatSessionBase):
    user_id: UUID
    other_user_id: UUID | None = None


class ChatSessionRead(ChatSessionBase):
    id: UUID
    user_id: UUID
    other_user_id: UUID | None
    created_at: datetime

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    session_id: UUID
    sender_id: UUID
    receiver_id: UUID


class MessageRead(MessageBase):
    id: UUID
    session_id: UUID
    sender_id: UUID
    receiver_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SearchBase(BaseModel):
    query: str | None = None
    type: SearchType = SearchType.DEFAULT
    target: SearchTarget
    country: str | None = None
    city: str | None = None
    town: str | None = None
    contract_type: PositionType | None = None
    education_level: str | None = None
    experience: str | None = None
    language: str | None = None
    date_publication: datetime | None = None


class SearchCreate(SearchBase):
    user_id: UUID


class SearchRead(SearchBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class OfferTemplateBase(BaseModel):
    title: str
    description: str | None = None
    mobility: Mobility | None = None
    position_type: PositionType
    seniority: SeniorityLevel | None = None
    duration_months: int | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    salary_avg: Decimal | None = None
    salary_type: SalaryType | None = None
    experience_years: int | None = None
    priority_level: int | None = None
    country: str | None = None
    city: str | None = None
    town: str | None = None
    address: str | None = None
    language: str | None = None
    ended_at: datetime | None = None


class OfferTemplateCreate(OfferTemplateBase):
    recruiter_id: UUID


class OfferTemplateRead(OfferTemplateBase):
    id: UUID
    recruiter_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class OfferBase(BaseModel):
    title: str
    description: str | None = None
    mobility: Mobility | None = None
    position_type: PositionType
    seniority: SeniorityLevel | None = None
    duration_months: int | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    salary_avg: Decimal | None = None
    salary_type: SalaryType | None = None
    experience_years: int | None = None
    priority_level: int | None = None
    country: str | None = None
    city: str | None = None
    town: str | None = None
    address: str | None = None
    language: str | None = None
    ended_at: datetime | None = None


class OfferCreate(OfferBase):
    recruiter_id: UUID
    template_id: UUID | None = None


class OfferRead(OfferBase):
    id: UUID
    template_id: UUID | None
    recruiter_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class OfferSkillBase(BaseModel):
    title: str


class OfferSkillCreate(OfferSkillBase):
    offer_id: UUID


class OfferSkillRead(OfferSkillBase):
    id: UUID
    offer_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateSkillBase(BaseModel):
    title: str


class CandidateSkillCreate(CandidateSkillBase):
    candidate_id: UUID


class CandidateSkillRead(CandidateSkillBase):
    id: UUID
    candidate_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DesiredPositionBase(BaseModel):
    title: str
    level: SeniorityLevel | None = None


class DesiredPositionCreate(DesiredPositionBase):
    candidate_id: UUID


class DesiredPositionRead(DesiredPositionBase):
    id: UUID
    candidate_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DesiredPositionTypeBase(BaseModel):
    type: PositionType


class DesiredPositionTypeCreate(DesiredPositionTypeBase):
    candidate_id: UUID


class DesiredPositionTypeRead(DesiredPositionTypeBase):
    id: UUID
    candidate_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EducationBase(BaseModel):
    title: str
    school: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class EducationCreate(EducationBase):
    candidate_id: UUID


class EducationRead(EducationBase):
    id: UUID
    candidate_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ExperienceBase(BaseModel):
    title: str
    company: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class ExperienceCreate(ExperienceBase):
    candidate_id: UUID


class ExperienceRead(ExperienceBase):
    id: UUID
    candidate_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class ProjectCreate(ProjectBase):
    candidate_id: UUID


class ProjectRead(ProjectBase):
    id: UUID
    candidate_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class LanguageBase(BaseModel):
    title: str
    level: LanguageLevel | None = None


class LanguageCreate(LanguageBase):
    candidate_id: UUID


class LanguageRead(LanguageBase):
    id: UUID
    candidate_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
