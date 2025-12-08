import uuid
from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID, OID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
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


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=False))
    updated_at = Column(DateTime(timezone=False))
    deleted = Column(Boolean, nullable=False)
    deleted_at = Column(DateTime(timezone=False))
    email = Column(String(255), nullable=False, unique=True)
    email_verified_at = Column(DateTime(timezone=False))
    password = Column(String(255))
    provider = Column(Enum(Provider, name="provider_enum"), nullable=False)
    role = Column(Enum(UserRole, name="user_role_enum"), nullable=False)
    user_type = Column(Enum(UserType, name="user_type_enum"))

    candidate = relationship("Candidate", back_populates="user", uselist=False)
    recruiter = relationship("Recruiter", back_populates="user", uselist=False)
    sessions = relationship("UserSession", back_populates="user")
    searches = relationship("Search", back_populates="user")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=False))
    updated_at = Column(DateTime(timezone=False))
    avatar_url = Column(String(255))
    birth_date = Column(DateTime(timezone=False))
    completion_rate = Column(Float)
    cv_url = Column(String(255))
    experience_level = Column(
        Enum(ExperienceLevel, name="candidate_experience_level_enum")
    )
    first_name = Column(String(255))
    is_visible = Column(Boolean)
    last_viewed_month = Column(Date)
    monthly_profile_views = Column(Integer)
    profile_views = Column(Integer)
    last_name = Column(String(255))
    linked_in_url = Column(String(255))
    city = Column(String(255))
    country = Column(String(255))
    region = Column(String(255))
    motivation_letter_url = Column(String(255))
    phone_number = Column(String(255))
    pitch_mail = Column(String(2000))
    portfolio_url = Column(String(255))
    presentation = Column(String(255))
    professional_title = Column(String(255))
    school_level = Column(
        Enum(SchoolLevel, name="candidate_school_level_enum")
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="candidate")
    educations = relationship("Education", back_populates="candidate")
    experiences = relationship("Experience", back_populates="candidate")
    skills = relationship("Skill", back_populates="candidate")
    languages = relationship("Language", back_populates="candidate")
    job_preferences = relationship("JobPreferences", back_populates="candidate", uselist=False)
    applications = relationship("Application", back_populates="candidate")
    saved_job_offers = relationship("SavedJobOffer", back_populates="candidate")


class Education(Base):
    __tablename__ = "education"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    city = Column(String(255))
    degree = Column(String(255))
    graduation_year = Column(Integer)
    institution = Column(String(255))
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="educations")


class Experience(Base):
    __tablename__ = "experience"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    city = Column(String(255))
    company_name = Column(String(255))
    description = Column(String(255))
    end_date = Column(DateTime(timezone=True))
    is_current = Column(Boolean)
    position = Column(String(255))
    start_date = Column(DateTime(timezone=True), nullable=False)
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="experiences")


class Skill(Base):
    __tablename__ = "skill"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    level = Column(Enum(SkillLevel, name="skill_level_enum"))
    name = Column(String(255))
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="skills")


class Language(Base):
    __tablename__ = "language"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    language = Column(String(255))
    level = Column(Enum(LanguageLevel, name="language_level_enum"))
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="languages")


class JobPreferences(Base):
    __tablename__ = "job_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    availability = Column(String(255))
    desired_position = Column(String(255))
    city = Column(String(255))
    country = Column(String(255))
    region = Column(String(255))
    pretentions_salarial = Column(String(255))
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="job_preferences")
    contract_types = relationship(
        "JobPreferencesContractType",
        back_populates="job_preferences",
        cascade="all, delete-orphan",
    )
    sectors = relationship(
        "JobPreferencesSector",
        back_populates="job_preferences",
        cascade="all, delete-orphan",
    )


class JobPreferencesContractType(Base):
    __tablename__ = "job_preferences_contract_types"

    job_preferences_id = Column(
        UUID(as_uuid=True), ForeignKey("job_preferences.id"), primary_key=True
    )
    contract_type = Column(
        Enum(ContractType, name="job_preferences_contract_enum"), primary_key=True
    )

    job_preferences = relationship(
        "JobPreferences", back_populates="contract_types"
    )


class JobPreferencesSector(Base):
    __tablename__ = "job_preferences_sectors"

    job_preferences_id = Column(
        UUID(as_uuid=True), ForeignKey("job_preferences.id"), primary_key=True
    )
    sector_id = Column(
        UUID(as_uuid=True), ForeignKey("sector.id"), primary_key=True
    )

    job_preferences = relationship("JobPreferences", back_populates="sectors")
    sector = relationship("Sector", back_populates="job_preferences_links")


class Sector(Base):
    __tablename__ = "sector"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    description = Column(String(255))
    name = Column(String(255))

    recruiters = relationship("Recruiter", back_populates="sector")
    job_preferences_links = relationship(
        "JobPreferencesSector",
        back_populates="sector",
        cascade="all, delete-orphan",
    )


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    company_description = Column(String(255))
    company_email = Column(String(255))
    company_length = Column(Integer)
    company_linked_in_url = Column(String(255))
    company_logo_url = Column(String(255))
    company_name = Column(String(255))
    company_phone = Column(String(255))
    company_website = Column(String(255))
    first_name = Column(String(255))
    function = Column(String(255))
    last_name = Column(String(255))
    city = Column(String(255))
    country = Column(String(255))
    region = Column(String(255))
    phone_number = Column(String(255))
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sector.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="recruiter")
    sector = relationship("Sector", back_populates="recruiters")
    job_offers = relationship(
        "JobOffer", back_populates="recruiter", cascade="all, delete-orphan"
    )


class JobOffer(Base):
    __tablename__ = "job_offer"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    contract_type = Column(Enum(ContractType, name="job_offer_contract_enum"))
    description = Column(String(255))
    expiration_date = Column(DateTime(timezone=False))
    instructions = Column(String(255))
    is_featured = Column(Boolean)
    is_urgent = Column(Boolean)
    job_type = Column(Enum(JobType, name="job_offer_type_enum"))
    post_number = Column(Integer)
    published_at = Column(DateTime(timezone=False))
    required_language = Column(String(255))
    salary = Column(String(255))
    status = Column(Enum(JobOfferStatus, native_enum=False))
    title = Column(String(255))
    work_city_location = Column(String(255))
    work_country_location = Column(String(255))
    benefits = Column(OID)
    requirements = Column(OID)
    responsibilities = Column(OID)
    company_id = Column(
        UUID(as_uuid=True), ForeignKey("recruiters.id"), nullable=False
    )

    recruiter = relationship("Recruiter", back_populates="job_offers")
    applications = relationship(
        "Application", back_populates="job_offer", cascade="all, delete-orphan"
    )
    saved_by = relationship(
        "SavedJobOffer", back_populates="job_offer", cascade="all, delete-orphan"
    )
    tag_links = relationship(
        "JobOfferTag",
        back_populates="job_offer",
        cascade="all, delete-orphan",
    )
    tags = relationship(
        "Tag",
        secondary="job_offer_tags",
        back_populates="job_offers",
        overlaps="tag_links",
    )
    candidature_info = relationship(
        "CandidatureInfo",
        back_populates="job_offer",
        uselist=False,
        cascade="all, delete-orphan",
    )
    required_documents = relationship(
        "RequiredDocument",
        back_populates="job_offer",
        cascade="all, delete-orphan",
    )


class JobOfferTag(Base):
    __tablename__ = "job_offer_tags"

    job_offer_id = Column(UUID(as_uuid=True), ForeignKey("job_offer.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tag.id"), primary_key=True)

    job_offer = relationship("JobOffer", back_populates="tag_links", overlaps="tags")
    tag = relationship("Tag", back_populates="job_offer_links", overlaps="tags")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    name = Column(String(255), nullable=False)
    type = Column(String(255))

    job_offer_links = relationship(
        "JobOfferTag",
        back_populates="tag",
        cascade="all, delete-orphan",
        overlaps="tags",
    )
    job_offers = relationship(
        "JobOffer",
        secondary="job_offer_tags",
        back_populates="tags",
        overlaps="job_offer_links,tag,job_offer,tag_links",
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    applied_at = Column(DateTime(timezone=False))
    message = Column(String(255))
    status = Column(Enum(ApplicationStatus, name="application_status_enum"))
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    job_offer_id = Column(
        UUID(as_uuid=True), ForeignKey("job_offer.id"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="applications")
    job_offer = relationship("JobOffer", back_populates="applications")
    documents = relationship(
        "ApplicationDocument",
        back_populates="application",
        cascade="all, delete-orphan",
    )


class ApplicationDocument(Base):
    __tablename__ = "application_document"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    storage_url = Column(String(255))
    type = Column(
        Enum(
            DocumentType,
            name="application_document_type_enum",
            native_enum=False,
        )
    )
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"))

    application = relationship("Application", back_populates="documents")


class CandidatureInfo(Base):
    __tablename__ = "candidature_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    job_offer_id = Column(
        UUID(as_uuid=True), ForeignKey("job_offer.id"), nullable=False, unique=True
    )
    email_candidature = Column(String(255))
    instructions = Column(String(255))
    required_documents = Column(String(255))
    url_candidature = Column(String(255))

    job_offer = relationship("JobOffer", back_populates="candidature_info")


class RequiredDocument(Base):
    __tablename__ = "required_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    job_offer_id = Column(UUID(as_uuid=True), ForeignKey("job_offer.id"))
    type = Column(
        Enum(
            DocumentType,
            name="required_documents_type_enum",
            native_enum=False,
        )
    )

    job_offer = relationship("JobOffer", back_populates="required_documents")


class SavedJobOffer(Base):
    __tablename__ = "saved_job_offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    job_offer_id = Column(
        UUID(as_uuid=True), ForeignKey("job_offer.id"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="saved_job_offers")
    job_offer = relationship("JobOffer", back_populates="saved_by")


class Search(Base):
    __tablename__ = "searches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(String(255), nullable=False)
    type = Column(Enum(SearchType, name="search_type_enum"), nullable=False)
    target = Column(Enum(SearchTarget, name="search_target_enum"), nullable=False)
    country = Column(String(255))
    city = Column(String(255))
    town = Column(String(255))
    type_contrat = Column(String(255))
    niveau_etude = Column(String(255))
    experience = Column(String(255))
    language = Column(String(255))
    date_publication = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="searches")


class EmailOtp(Base):
    __tablename__ = "email_otp"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(255), nullable=False)
    consumed = Column(Boolean, nullable=False, default=False)
    email = Column(String(255), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    purpose = Column(Enum(OtpPurpose, native_enum=False), nullable=False)
    user_type = Column(Enum(UserType, name="email_otp_user_type_enum"))


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    device_info = Column(String(255))
    expired_at = Column(DateTime(timezone=True))
    ip_address = Column(String(255))
    is_active = Column(Boolean, default=True)
    token = Column(String(255))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="sessions")
