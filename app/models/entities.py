import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
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


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=True)
    role = Column(
        Enum(UserRole, name="user_role_enum"),
        nullable=False,
        default=UserRole.CANDIDATE,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    candidate_profile = relationship(
        "Candidate", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    recruiter_profile = relationship(
        "Recruiter", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    recommendations = relationship(
        "Recommendation", back_populates="user", cascade="all, delete-orphan"
    )
    searches = relationship(
        "Search", back_populates="user", cascade="all, delete-orphan"
    )
    chat_sessions = relationship(
        "ChatSession",
        back_populates="user",
        foreign_keys="ChatSession.user_id",
        cascade="all, delete-orphan",
    )
    chat_sessions_as_other = relationship(
        "ChatSession",
        back_populates="other_user",
        foreign_keys="ChatSession.other_user_id",
    )
    sent_messages = relationship(
        "Message",
        back_populates="sender",
        foreign_keys="Message.sender_id",
        cascade="all, delete-orphan",
    )
    received_messages = relationship(
        "Message",
        back_populates="receiver",
        foreign_keys="Message.receiver_id",
        cascade="all, delete-orphan",
    )


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    mobility = Column(
        Enum(Mobility, name="candidate_mobility_enum"), nullable=True
    )
    country = Column(String(150), nullable=True)
    city = Column(String(150), nullable=True)
    town = Column(String(150), nullable=True)
    address = Column(String(255), nullable=True)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_avg = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    notification_delay = Column(
        Enum(NotificationDelay, name="notification_delay_enum"), nullable=True
    )
    notification_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="candidate_profile")
    skills = relationship(
        "CandidateSkill", back_populates="candidate", cascade="all, delete-orphan"
    )
    desired_positions = relationship(
        "DesiredPosition", back_populates="candidate", cascade="all, delete-orphan"
    )
    desired_position_types = relationship(
        "DesiredPositionType", back_populates="candidate", cascade="all, delete-orphan"
    )
    educations = relationship(
        "Education", back_populates="candidate", cascade="all, delete-orphan"
    )
    experiences = relationship(
        "Experience", back_populates="candidate", cascade="all, delete-orphan"
    )
    projects = relationship(
        "Project", back_populates="candidate", cascade="all, delete-orphan"
    )
    languages = relationship(
        "Language", back_populates="candidate", cascade="all, delete-orphan"
    )


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    organization_name = Column(String(255), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="recruiter_profile")
    offer_templates = relationship(
        "OfferTemplate", back_populates="recruiter", cascade="all, delete-orphan"
    )
    offers = relationship(
        "Offer", back_populates="recruiter", cascade="all, delete-orphan"
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    label = Column(String(255), nullable=False)
    target = Column(
        Enum(RecommendationTarget, name="recommendation_target_enum"), nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    number = Column(Integer, nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="recommendations")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    other_user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    token = Column(String(255), nullable=False, unique=True)
    bot = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship(
        "User", foreign_keys=[user_id], back_populates="chat_sessions"
    )
    other_user = relationship(
        "User", foreign_keys=[other_user_id], back_populates="chat_sessions_as_other"
    )
    messages = relationship(
        "Message", back_populates="session", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id = Column(
        UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False
    )
    sender_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    receiver_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    session = relationship("ChatSession", back_populates="messages")
    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_messages"
    )
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_messages"
    )


class Search(Base):
    __tablename__ = "searches"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    query = Column(String(255), nullable=True)
    type = Column(
        Enum(SearchType, name="search_type_enum"),
        nullable=False,
        default=SearchType.DEFAULT,
    )
    target = Column(
        Enum(SearchTarget, name="search_target_enum"), nullable=False
    )
    country = Column(String(150), nullable=True)
    city = Column(String(150), nullable=True)
    town = Column(String(150), nullable=True)
    contract_type = Column(
        Enum(PositionType, name="search_contract_enum"), nullable=True
    )
    education_level = Column(String(150), nullable=True)
    experience = Column(String(150), nullable=True)
    language = Column(String(150), nullable=True)
    date_publication = Column(
        DateTime(timezone=True), nullable=True
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="searches")


class OfferTemplate(Base):
    __tablename__ = "offer_templates"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recruiter_id = Column(
        UUID(as_uuid=True), ForeignKey("recruiters.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    mobility = Column(
        Enum(Mobility, name="offer_mobility_enum"), nullable=True
    )
    position_type = Column(
        Enum(PositionType, name="offer_position_type_enum"), nullable=False
    )
    seniority = Column(
        Enum(SeniorityLevel, name="offer_seniority_enum"), nullable=True
    )
    duration_months = Column(Integer, nullable=True)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    salary_avg = Column(Numeric(12, 2), nullable=True)
    salary_type = Column(
        Enum(SalaryType, name="offer_salary_type_enum"), nullable=True
    )
    experience_years = Column(Integer, nullable=True)
    priority_level = Column(Integer, nullable=True)
    country = Column(String(150), nullable=True)
    city = Column(String(150), nullable=True)
    town = Column(String(150), nullable=True)
    address = Column(String(255), nullable=True)
    language = Column(String(150), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ended_at = Column(
        DateTime(timezone=True), nullable=True
    )

    recruiter = relationship("Recruiter", back_populates="offer_templates")
    offers = relationship(
        "Offer", back_populates="template", cascade="all, delete-orphan"
    )


class Offer(Base):
    __tablename__ = "offers"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    template_id = Column(
        UUID(as_uuid=True), ForeignKey("offer_templates.id"), nullable=True
    )
    recruiter_id = Column(
        UUID(as_uuid=True), ForeignKey("recruiters.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    mobility = Column(
        Enum(Mobility, name="offer_instance_mobility_enum"), nullable=True
    )
    position_type = Column(
        Enum(PositionType, name="offer_instance_position_type_enum"), nullable=False
    )
    seniority = Column(
        Enum(SeniorityLevel, name="offer_instance_seniority_enum"), nullable=True
    )
    duration_months = Column(Integer, nullable=True)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    salary_avg = Column(Numeric(12, 2), nullable=True)
    salary_type = Column(
        Enum(SalaryType, name="offer_instance_salary_type_enum"), nullable=True
    )
    experience_years = Column(Integer, nullable=True)
    priority_level = Column(Integer, nullable=True)
    country = Column(String(150), nullable=True)
    city = Column(String(150), nullable=True)
    town = Column(String(150), nullable=True)
    address = Column(String(255), nullable=True)
    language = Column(String(150), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ended_at = Column(
        DateTime(timezone=True), nullable=True
    )

    template = relationship("OfferTemplate", back_populates="offers")
    recruiter = relationship("Recruiter", back_populates="offers")
    skills = relationship(
        "OfferSkill", back_populates="offer", cascade="all, delete-orphan"
    )


class OfferSkill(Base):
    __tablename__ = "offer_skills"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    offer_id = Column(
        UUID(as_uuid=True), ForeignKey("offers.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    offer = relationship("Offer", back_populates="skills")


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate = relationship("Candidate", back_populates="skills")


class DesiredPosition(Base):
    __tablename__ = "desired_positions"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    level = Column(
        Enum(SeniorityLevel, name="desired_position_level_enum"), nullable=True
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate = relationship("Candidate", back_populates="desired_positions")


class DesiredPositionType(Base):
    __tablename__ = "desired_position_types"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    type = Column(
        Enum(PositionType, name="desired_position_type_enum"), nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate = relationship("Candidate", back_populates="desired_position_types")


class Education(Base):
    __tablename__ = "educations"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    school = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate = relationship("Candidate", back_populates="educations")


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate = relationship("Candidate", back_populates="experiences")


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate = relationship("Candidate", back_populates="projects")


class Language(Base):
    __tablename__ = "languages"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    level = Column(
        Enum(LanguageLevel, name="language_level_enum"), nullable=True
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    candidate = relationship("Candidate", back_populates="languages")
