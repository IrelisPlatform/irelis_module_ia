from enum import Enum


class Mobility(str, Enum):
    ON_SITE = "on-site"
    REMOTE = "remote"
    HYBRID = "hybrid"


class SeniorityLevel(str, Enum):
    JUNIOR = "junior"
    SENIOR = "senior"


class PositionType(str, Enum):
    CDI = "cdi"
    CDD = "cdd"
    STAGE = "stage"
    FREELANCE = "freelance"
    ALTERNANCE = "alternance"
    OTHER = "other"


class SalaryType(str, Enum):
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    INTERVAL = "interval"


class NotificationDelay(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class RecommendationTarget(str, Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"


class SearchType(str, Enum):
    BOOLEAN = "boolean"
    DEFAULT = "default"


class SearchTarget(str, Enum):
    OFFER = "offer"
    CANDIDATE = "candidate"


class LanguageLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class UserRole(str, Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"
    ADMIN = "admin"
