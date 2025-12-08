from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CANDIDATE = "CANDIDATE"
    RECRUITER = "RECRUITER"


class UserType(str, Enum):
    ADMIN = "ADMIN"
    CANDIDATE = "CANDIDATE"
    RECRUITER = "RECRUITER"


class Provider(str, Enum):
    EMAIL = "EMAIL"
    FACEBOOK = "FACEBOOK"
    GOOGLE = "GOOGLE"
    LINKEDIN = "LINKEDIN"


class ApplicationStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    REVIEWED = "REVIEWED"
    WITHDRAWN = "WITHDRAWN"


class ExperienceLevel(str, Enum):
    ADVANCED = "ADVANCED"
    BEGINNER = "BEGINNER"
    EXPERT = "EXPERT"
    INTERMEDIATE = "INTERMEDIATE"
    JUNIOR = "JUNIOR"
    SENIOR = "SENIOR"


class SchoolLevel(str, Enum):
    BAC = "BAC"
    BTS = "BTS"
    DEUG = "DEUG"
    DOCTORAL = "DOCTORAL"
    DUT = "DUT"
    LICENCE = "LICENCE"
    MASTER = "MASTER"
    UNKNOWN = "UNKNOWN"


class ContractType(str, Enum):
    ALTERNATIVE = "ALTERNATIVE"
    CDD = "CDD"
    CDI = "CDI"
    FREELANCE = "FREELANCE"
    INTERNSHIP = "INTERNSHIP"


class JobType(str, Enum):
    FULL_TIME = "FULL_TIME"
    HYBRID = "HYBRID"
    PART_TIME = "PART_TIME"
    REMOTE = "REMOTE"


class JobOfferStatus(str, Enum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"


class SkillLevel(str, Enum):
    ADVANCED = "ADVANCED"
    BEGINNER = "BEGINNER"
    EXPERT = "EXPERT"
    INTERMEDIATE = "INTERMEDIATE"


class LanguageLevel(str, Enum):
    ADVANCED = "ADVANCED"
    BEGINNER = "BEGINNER"
    BILINGUAL = "BILINGUAL"
    INTERMEDIATE = "INTERMEDIATE"
    NATIVE_LANGUAGE = "NATIVE_LANGUAGE"


class DocumentType(str, Enum):
    CV = "CV"
    COVER_LETTER = "COVER_LETTER"
    PORTFOLIO = "PORTFOLIO"
    CERTIFICATE = "CERTIFICATE"
    IDENTITY_DOC = "IDENTITY_DOC"


class OtpPurpose(str, Enum):
    LOGIN_REGISTER = "LOGIN_REGISTER"
    PASSWORD_RESET = "PASSWORD_RESET"
    OAUTH2 = "OAUTH2"


class SearchType(str, Enum):
    BOOL = "BOOL"
    NOT = "NOT"


class SearchTarget(str, Enum):
    OFFRE = "OFFRE"
    CANDIDAT = "CANDIDAT"
