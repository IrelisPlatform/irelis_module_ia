"""
Extended seed script to populate PostgreSQL with realistic data.

Usage:
    python -m app.db.seed
The script is idempotent: it aborts if users already exist.
"""

from __future__ import annotations

import logging
import random
from datetime import date
from decimal import Decimal
from typing import Iterable

from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models import (
    Candidate,
    CandidateSkill,
    ChatSession,
    DesiredPosition,
    DesiredPositionType,
    Education,
    Experience,
    Language,
    Message,
    Offer,
    OfferSkill,
    OfferTemplate,
    Project,
    Recommendation,
    Recruiter,
    Search,
    User,
)
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

logger = logging.getLogger(__name__)
random.seed(42)

CANDIDATE_FIRST_NAMES = [
    "Alice",
    "Yann",
    "Maya",
    "Lamine",
    "Ines",
    "Boris",
    "Sarah",
    "Julien",
    "Clara",
    "Hugo",
    "Nina",
    "Ethan",
    "Awa",
    "Noah",
    "Emma",
    "Eli",
    "Adama",
    "Lea",
    "Tom",
    "Amadou",
]
CANDIDATE_LAST_NAMES = [
    "Martin",
    "Diallo",
    "Nguyen",
    "Kane",
    "Benali",
    "Moreau",
    "Konate",
    "Dupont",
    "Benitez",
    "Fischer",
    "Sarr",
    "Petit",
    "Diop",
    "Lam",
    "Renard",
    "Perrin",
    "Faye",
    "Chevalier",
    "Rolland",
    "Traore",
]
CANDIDATE_SKILLS = [
    "Python",
    "FastAPI",
    "Django",
    "PostgreSQL",
    "Redis",
    "Docker",
    "Kubernetes",
    "AWS",
    "Terraform",
    "React",
    "Vue",
    "TypeScript",
    "Node.js",
    "GraphQL",
    "CI/CD",
    "MLflow",
]
CANDIDATE_LANGUAGES = [LanguageLevel.A1, LanguageLevel.A2, LanguageLevel.B1, LanguageLevel.B2, LanguageLevel.C1, LanguageLevel.C2]
CITIES = [
    ("France", "Paris"),
    ("France", "Lyon"),
    ("France", "Marseille"),
    ("Sénégal", "Dakar"),
    ("Côte d'Ivoire", "Abidjan"),
    ("Maroc", "Casablanca"),
    ("Tunisie", "Tunis"),
    ("Belgique", "Bruxelles"),
]
POSITION_TITLES = [
    "Développeur Backend",
    "Ingénieur Data",
    "Développeur Fullstack",
    "Product Manager",
    "Architecte Logiciel",
    "DevOps Engineer",
]
PROJECT_TITLES = [
    "Plateforme RH",
    "Dashboard IoT",
    "Marketplace Artisanale",
    "Application Mobile Santé",
    "Portail Analytique",
]
LANGUAGE_NAMES = ["Français", "Anglais", "Espagnol", "Arabe", "Wolof", "Allemand"]

RECRUITER_FIRST_NAMES = [
    "Marc",
    "Sophie",
    "Karim",
    "Fatou",
    "Luc",
    "Aminata",
    "Pierre",
    "Lena",
    "Omar",
    "Chloé",
    "Victor",
    "Salimata",
    "Bastien",
    "Nadia",
    "Loïc",
    "Rokia",
    "Mamadou",
]
RECRUITER_LAST_NAMES = [
    "Dupont",
    "Morel",
    "Bensaid",
    "Cissé",
    "Bernard",
    "Gueye",
    "Robert",
    "Marchand",
    "Fall",
    "Perrot",
    "Masson",
    "Sow",
    "Fontaine",
    "Bouaziz",
    "Collet",
    "Diakité",
    "Camara",
]
COMPANIES = [
    "TechHire",
    "Talent Africa",
    "NextPeople",
    "SkillBridge",
    "NovaJobs",
    "LinkPartners",
    "DigitalQuest",
    "ZenithRH",
    "PulseRecruit",
    "BrightFuture",
]
OFFER_SKILLS = [
    "FastAPI",
    "React",
    "Kubernetes",
    "Terraform",
    "Airflow",
    "Spark",
    "Java",
    "Go",
    "Rust",
    "Figma",
]


def _add_all(session: Session, items: Iterable[object]) -> None:
    for item in items:
        session.add(item)


def _email(first: str, last: str, suffix: str) -> str:
    slug = f"{first}.{last}".replace(" ", "").lower()
    return f"{slug}.{suffix}@example.com"


def _decimal_amount(base: int, spread: int, idx: int) -> Decimal:
    return Decimal(str(base + spread * idx))


def seed_candidates(db: Session, count: int = 20) -> list[tuple[User, Candidate]]:
    results: list[tuple[User, Candidate]] = []
    mobility_values = list(Mobility)
    notify_values = list(NotificationDelay)
    position_types = list(PositionType)
    levels = list(SeniorityLevel)

    for idx in range(count):
        first = CANDIDATE_FIRST_NAMES[idx % len(CANDIDATE_FIRST_NAMES)]
        last = CANDIDATE_LAST_NAMES[idx % len(CANDIDATE_LAST_NAMES)]
        country, city = CITIES[idx % len(CITIES)]
        user = User(
            first_name=first,
            last_name=last,
            email=_email(first, last, f"cand{idx}"),
            phone=f"06{idx:02d}{idx+11:02d}{idx+22:02d}",
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.flush()

        salary_floor = _decimal_amount(30000, 900, idx)
        candidate = Candidate(
            user_id=user.id,
            mobility=random.choice(mobility_values),
            country=country,
            city=city,
            address=f"{12+idx} rue Exemple",
            salary_min=salary_floor,
            salary_avg=salary_floor + Decimal("3000"),
            salary_max=salary_floor + Decimal("6000"),
            notification_delay=random.choice(notify_values),
            notification_enabled=True,
        )
        db.add(candidate)
        db.flush()

        skill_choices = random.sample(CANDIDATE_SKILLS, k=4)
        _add_all(
            db,
            (CandidateSkill(candidate_id=candidate.id, title=skill) for skill in skill_choices),
        )

        desired_roles = random.sample(POSITION_TITLES, k=2)
        _add_all(
            db,
            (
                DesiredPosition(
                    candidate_id=candidate.id,
                    title=role,
                    level=random.choice(levels),
                )
                for role in desired_roles
            ),
        )

        desired_types = random.sample(position_types, k=2)
        _add_all(
            db,
            (DesiredPositionType(candidate_id=candidate.id, type=ptype) for ptype in desired_types),
        )

        education = Education(
            candidate_id=candidate.id,
            title="Master Informatique",
            school=f"Université {city}",
            description="Spécialité IA et cloud",
            start_date=date(2015 + (idx % 4), 9, 1),
            end_date=date(2017 + (idx % 4), 7, 1),
        )
        db.add(education)

        experience = Experience(
            candidate_id=candidate.id,
            title=random.choice(POSITION_TITLES),
            company=f"Startup {idx % 15 + 1}",
            description="Contribution à des API scalables",
            start_date=date(2018, 1, 1),
            end_date=None,
        )
        db.add(experience)

        project = Project(
            candidate_id=candidate.id,
            title=random.choice(PROJECT_TITLES),
            description="PoC data/IA pour un client international",
            start_date=date(2020, 6, 1),
            end_date=date(2021, 1, 1),
        )
        db.add(project)

        languages = random.sample(LANGUAGE_NAMES, k=2)
        _add_all(
            db,
            (
                Language(
                    candidate_id=candidate.id,
                    title=lang,
                    level=random.choice(CANDIDATE_LANGUAGES),
                )
                for lang in languages
            ),
        )

        results.append((user, candidate))

    return results


def seed_recruiters(db: Session, count: int = 17) -> list[tuple[User, Recruiter]]:
    mobility_values = list(Mobility)
    position_types = list(PositionType)
    seniorities = list(SeniorityLevel)
    salary_types = list(SalaryType)
    results: list[tuple[User, Recruiter]] = []

    for idx in range(count):
        first = RECRUITER_FIRST_NAMES[idx % len(RECRUITER_FIRST_NAMES)]
        last = RECRUITER_LAST_NAMES[idx % len(RECRUITER_LAST_NAMES)]
        org = f"{COMPANIES[idx % len(COMPANIES)]} RH"
        user = User(
            first_name=first,
            last_name=last,
            email=_email(first, last, f"recr{idx}"),
            phone=f"01{idx:02d}{idx+33:02d}{idx+55:02d}",
            role=UserRole.RECRUITER,
        )
        db.add(user)
        db.flush()

        recruiter = Recruiter(user_id=user.id, organization_name=org)
        db.add(recruiter)
        db.flush()

        offers_to_create = 0 if idx == 0 else random.randint(1, 4)
        template = OfferTemplate(
            recruiter_id=recruiter.id,
            title=f"Template {org.split()[0]}",
            description="Modèle d'offre générique",
            mobility=random.choice(mobility_values),
            position_type=random.choice(position_types),
            seniority=random.choice(seniorities),
            duration_months=random.choice([6, 9, 12, 18]),
            salary_min=_decimal_amount(33000, 1100, idx),
            salary_max=_decimal_amount(42000, 1100, idx),
            salary_avg=_decimal_amount(36000, 1100, idx),
            salary_type=random.choice(salary_types),
            experience_years=random.randint(1, 8),
            priority_level=random.randint(1, 10),
            country=random.choice(CITIES)[0],
            city=random.choice(CITIES)[1],
            address=f"{20+idx} avenue Talents",
            language="fr",
        )
        db.add(template)
        db.flush()

        template_skill_names = random.sample(OFFER_SKILLS, k=3)
        _add_all(
            db,
            (OfferSkill(template_id=template.id, title=skill) for skill in template_skill_names),
        )

        for offer_idx in range(offers_to_create):
            offer = Offer(
                recruiter_id=recruiter.id,
                template_id=template.id,
                title=f"Offre {org.split()[0]} #{offer_idx+1}",
                description="Mission stratégique pour client international",
                mobility=random.choice(mobility_values),
                position_type=random.choice(position_types),
                seniority=random.choice(seniorities),
                duration_months=random.choice([6, 12, 18]),
                salary_min=_decimal_amount(35000, 900, offer_idx + idx),
                salary_max=_decimal_amount(48000, 900, offer_idx + idx),
                salary_avg=_decimal_amount(42000, 900, offer_idx + idx),
                salary_type=random.choice(salary_types),
                experience_years=random.randint(2, 7),
                priority_level=random.randint(1, 10),
                country=random.choice(CITIES)[0],
                city=random.choice(CITIES)[1],
                address=f"{50+offer_idx} boulevard Offre",
                language=random.choice(["fr", "en"]),
            )
            db.add(offer)
            db.flush()

            offer_skill_names = random.sample(OFFER_SKILLS, k=3)
            _add_all(
                db,
                (OfferSkill(offer_id=offer.id, title=skill) for skill in offer_skill_names),
            )

        results.append((user, recruiter))

    return results


def seed_relations(
    db: Session,
    candidate_profiles: list[tuple[User, Candidate]],
    recruiter_profiles: list[tuple[User, Recruiter]],
) -> None:
    # Searches
    searches = []
    for idx, (cand_user, cand) in enumerate(candidate_profiles):
        role = POSITION_TITLES[idx % len(POSITION_TITLES)]
        searches.append(
            Search(
                user_id=cand_user.id,
                query=f"{role} {cand.city}",
                type=SearchType.DEFAULT,
                target=SearchTarget.OFFER,
                country=cand.country,
                city=cand.city,
                contract_type=random.choice(list(PositionType)),
                experience="3+ ans",
                language="fr",
            )
        )
    for idx, (rec_user, _) in enumerate(recruiter_profiles[:10]):
        searches.append(
            Search(
                user_id=rec_user.id,
                query="Talents JS",
                type=SearchType.DEFAULT,
                target=SearchTarget.CANDIDATE,
                country="France",
                city="Paris",
                contract_type=PositionType.CDI,
                language="fr",
            )
        )
    _add_all(db, searches)

    # Recommendations
    recommendations = []
    for idx in range(12):
        rec_user, _ = recruiter_profiles[idx % len(recruiter_profiles)]
        cand_user, _ = candidate_profiles[idx % len(candidate_profiles)]
        recommendations.append(
            Recommendation(
                label=f"Recommandation candidat {cand_user.first_name}",
                target=RecommendationTarget.CANDIDATE,
                user_id=rec_user.id,
                number=random.randint(1, 5),
            )
        )
        recommendations.append(
            Recommendation(
                label=f"Recommandation recruteur {rec_user.first_name}",
                target=RecommendationTarget.RECRUITER,
                user_id=cand_user.id,
                number=random.randint(1, 5),
            )
        )
    _add_all(db, recommendations)

    # Chats & messages (10 pairs)
    for idx in range(10):
        cand_user, _ = candidate_profiles[idx]
        rec_user, _ = recruiter_profiles[idx]
        chat = ChatSession(
            user_id=cand_user.id,
            other_user_id=rec_user.id,
            token=f"CHAT-{idx:03d}",
            bot=False,
        )
        db.add(chat)
        db.flush()

        messages = [
            Message(
                session_id=chat.id,
                sender_id=cand_user.id,
                receiver_id=rec_user.id,
                content=f"Bonjour {rec_user.first_name}, je suis intéressé par l'offre #{idx+1}",
            ),
            Message(
                session_id=chat.id,
                sender_id=rec_user.id,
                receiver_id=cand_user.id,
                content="Merci pour votre message, planifions un échange !",
            ),
        ]
        _add_all(db, messages)


def seed_database() -> None:
    db = SessionLocal()
    try:
        init_db(db)
        if db.query(User).count() > 0:
            logger.warning("Seed skipped: database already contains data.")
            return

        logger.info("Seeding %s candidates", 20)
        candidate_profiles = seed_candidates(db, count=20)

        logger.info("Seeding %s recruiters", 17)
        recruiter_profiles = seed_recruiters(db, count=17)

        logger.info("Seeding relations (jobs/searches/reco/chats)")
        seed_relations(db, candidate_profiles, recruiter_profiles)

        db.commit()
        logger.info("Database seeded successfully.")
    except Exception:
        db.rollback()
        logger.exception("Seeding failed")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_database()
