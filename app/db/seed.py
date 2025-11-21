"""
Seed script focused on Cameroon job market.

Usage:
    python -m app.db.seed
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
random.seed(237)

CAMEROON_LOCATIONS = [
    ("Cameroun", "Yaoundé", "Centre"),
    ("Cameroun", "Douala", "Littoral"),
    ("Cameroun", "Garoua", "Nord"),
    ("Cameroun", "Bafoussam", "Ouest"),
    ("Cameroun", "Maroua", "Extrême-Nord"),
    ("Cameroun", "Bertoua", "Est"),
    ("Cameroun", "Ngaoundéré", "Adamaoua"),
    ("Cameroun", "Buea", "Sud-Ouest"),
    ("Cameroun", "Ebolowa", "Sud"),
    ("Cameroun", "Limbe", "Sud-Ouest"),
    ("Cameroun", "Kribi", "Sud"),
    ("Cameroun", "Kumba", "Sud-Ouest"),
    ("Cameroun", "Foumban", "Ouest"),
    ("Cameroun", "Dschang", "Ouest"),
    ("Cameroun", "Bamenda", "Nord-Ouest"),
    ("Cameroun", "Kousseri", "Extrême-Nord"),
    ("Cameroun", "Mbalmayo", "Centre"),
    ("Cameroun", "Sangmélima", "Sud"),
    ("Cameroun", "Mamfé", "Sud-Ouest"),
    ("Cameroun", "Kumba", "Sud-Ouest"),
    ("Cameroun", "Mokolo", "Extrême-Nord"),
    ("Cameroun", "Meiganga", "Adamaoua"),
    ("Cameroun", "Tiko", "Sud-Ouest"),
    ("Cameroun", "Akonolinga", "Centre"),
    ("Cameroun", "Obala", "Centre"),
    ("Cameroun", "Mbouda", "Ouest"),
    ("Cameroun", "Nkongsamba", "Littoral"),
    ("Cameroun", "Yagoua", "Extrême-Nord"),
    ("Cameroun", "Guider", "Nord"),
    ("Cameroun", "Kaélé", "Extrême-Nord"),
]

CAMEROON_COMPANIES = [
    "Afritech Labs",
    "CamTel Digital",
    "Gozem Cameroun",
    "NextWave Douala",
    "Startup Garage Yaoundé",
    "TelemedAfrique",
    "AgriSmart Cameroon",
    "PayPlus CM",
    "Mboa Logistics",
    "Energia Cameroun",
    "Maison Douce Services",
    "Resto Express",
    "CamRetail",
    "GreenHouse CM",
    "MotoLivreur",
    "NannyCare Cameroun",
    "BarberHub",
    "Glamour Beauty CM",
    "Soleil Voyages",
    "Express Pharma CM",
    "Yaoundé Taxis Coop",
    "Douala Market Place",
    "Boulangerie Soleil",
    "CamWaterWorks",
    "Nordic Agro CM",
    "Village Artisans",
    "HR4Africa",
    "Hotel Mont Cameroun",
    "BlueWave Maritime",
]

JOB_PROFILES = [
    {
        "title": "Développeur Backend Python",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.HYBRID,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (4500000, 6200000),
    },
    {
        "title": "Développeur Frontend React",
        "skills": ["React", "TypeScript", "GraphQL"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.REMOTE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (3000000, 4200000),
    },
    {
        "title": "Ingénieur DevOps",
        "skills": ["Docker", "Kubernetes", "CI/CD"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.HYBRID,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (5200000, 7000000),
    },
    {
        "title": "Data Scientist",
        "skills": ["Python", "Pandas", "MLflow"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.REMOTE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (4800000, 6500000),
    },
    {
        "title": "Chef de Projet Digital",
        "skills": ["Scrum", "Communication", "Reporting"],
        "position_type": PositionType.CDD,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (3600000, 5000000),
    },
    {
        "title": "Analyste Cybersécurité",
        "skills": ["SIEM", "Python", "Risk Management"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.HYBRID,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (4000000, 5800000),
    },
    {
        "title": "Responsable Ressources Humaines",
        "skills": ["Gestion RH", "Communication", "Reporting"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (3500000, 4800000),
    },
    {
        "title": "Comptable Sénior",
        "skills": ["Comptabilité", "Excel", "Fiscalité"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (3200000, 4500000),
    },
    {
        "title": "Caissière Supermarché",
        "skills": ["Gestion de caisse", "Service client"],
        "position_type": PositionType.CDD,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1200000, 1800000),
    },
    {
        "title": "Serveur Restaurant",
        "skills": ["Service client", "Communication", "Gestion de commande"],
        "position_type": PositionType.CDD,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1400000, 2000000),
    },
    {
        "title": "Chef Cuisinier",
        "skills": ["Cuisine professionnelle", "Gestion équipe", "Hygiène"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (2800000, 3800000),
    },
    {
        "title": "Barbier",
        "skills": ["Coiffure", "Service client", "Hygiène"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1500000, 2200000),
    },
    {
        "title": "Livreur Moto",
        "skills": ["Conduite moto", "Livraison urbaine", "Relation client"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1300000, 1900000),
    },
    {
        "title": "Agent de Sécurité",
        "skills": ["Sécurité privée", "Surveillance", "Rapport"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1400000, 2100000),
    },
    {
        "title": "Ménagère",
        "skills": ["Entretien ménager", "Organisation", "Cuisine professionnelle"],
        "position_type": PositionType.CDD,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1100000, 1600000),
    },
    {
        "title": "Nounou",
        "skills": ["Soins infantiles", "Communication", "Organisation"],
        "position_type": PositionType.CDD,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1200000, 1700000),
    },
    {
        "title": "Chargé Marketing Terrain",
        "skills": ["Marketing terrain", "Vente", "Reporting"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.HYBRID,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (2200000, 3100000),
    },
    {
        "title": "Magasinier",
        "skills": ["Gestion de stocks", "Logistique urbaine", "Manutention"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1500000, 2100000),
    },
    {
        "title": "Chargé Logistique",
        "skills": ["Logistique urbaine", "Planification", "Excel"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.HYBRID,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (2800000, 3800000),
    },
    {
        "title": "Hôtesse d'accueil",
        "skills": ["Service client", "Communication", "Organisation"],
        "position_type": PositionType.CDD,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1300000, 1900000),
    },
    {
        "title": "Chauffeur Poids Lourd",
        "skills": ["Conduite poids lourd", "Logistique", "Maintenance"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (2000000, 2800000),
    },
    {
        "title": "Technicien Froid",
        "skills": ["Technicien froid", "Maintenance électroménager", "Sécurité"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (2400000, 3300000),
    },
    {
        "title": "Responsable Boutique",
        "skills": ["Gestion boutique", "Service client", "Stocks"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (2500000, 3400000),
    },
    {
        "title": "Animateur Commercial",
        "skills": ["Communication", "Vente", "Animation"],
        "position_type": PositionType.CDD,
        "mobility": Mobility.HYBRID,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1600000, 2300000),
    },
    {
        "title": "Chef de Rayon",
        "skills": ["Gestion de rayon", "Management équipe", "Merchandising"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.SENIOR,
        "salary_range": (2600000, 3600000),
    },
    {
        "title": "Assistante Administrative",
        "skills": ["Organisation", "Saisie", "Accueil"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1700000, 2300000),
    },
    {
        "title": "Livreur E-commerce",
        "skills": ["Livraison urbaine", "Service client", "Planification"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1500000, 2100000),
    },
    {
        "title": "Coiffeuse mixte",
        "skills": ["Coiffure", "Service client", "Manucure"],
        "position_type": PositionType.CDI,
        "mobility": Mobility.ON_SITE,
        "seniority": SeniorityLevel.JUNIOR,
        "salary_range": (1600000, 2300000),
    },
]

OFFER_SKILLS = sorted({skill for profile in JOB_PROFILES for skill in profile["skills"]})

POSITION_TITLES = [
    "Développeur Backend",
    "Ingénieur Data",
    "Développeur Fullstack",
    "Product Manager",
    "Architecte Logiciel",
    "DevOps Engineer",
    "Responsable RH",
    "Comptable Sénior",
    "Caissière",
    "Serveur en restauration",
    "Chef cuisinier",
    "Barbier",
    "Livreur urbain",
    "Agent de sécurité",
    "Ménagère",
    "Nounou",
    "Chargé de communication",
    "Responsable marketing",
    "Chargé logistique",
    "Magasinier",
    "Hôtesse d'accueil",
    "Chauffeur poids lourd",
    "Technicien froid",
    "Responsable boutique",
    "Animateur commercial",
    "Chef de rayon",
]

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
    "Hermann",
    "Sylvie",
    "Boris",
    "Clarisse",
    "Lionel",
    "Mireille",
    "Cédric",
]

RECRUITER_LAST_NAMES = [
    "Mbarga",
    "Tchoungui",
    "Njembe",
    "Siewe",
    "Njoh",
    "Egang",
    "Djouh",
    "Feuzeu",
    "Mouafo",
    "Etoga",
    "Biloa",
    "Tsala",
    "Dzuimo",
    "Kouatchoua",
    "Nke",
    "Mbassi",
    "Kenmogne",
    "Onana",
    "Messina",
    "Ndzie",
    "Tadjo",
    "Kaptue",
    "Nguimbous",
    "Jemba",
]

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
    "Patrick",
    "Sandrine",
    "Stephane",
    "Gaelle",
    "Rostand",
    "Linda",
    "Kevin",
    "Prisca",
    "Dorian",
    "Natacha",
    "Ludovic",
    "Rosine",
    "Cynthia",
    "Fabrice",
    "Aurélie",
    "Aline",
    "Grégory",
    "Georges",
    "Christian",
    "Olive",
    "Tatiana",
    "Vivien",
    "Brice",
    "Irène",
    "Gisèle",
    "Albert",
    "Justine",
    "Mireille",
    "Dany",
    "Valery",
    "Ketty",
    "Anicet",
    "Rosalie",
    "Ibrahim",
    "Serges",
    "Noëlle",
    "Gabin",
    "Prisca",
    "Edgard",
    "Viviane",
    "Marcel",
    "Josiane",
    "Olivier",
    "Laure",
    "Ange",
    "Nicolas",
    "Emeline",
]

CANDIDATE_LAST_NAMES = [
    "Mbarga",
    "Ngono",
    "Biloa",
    "Nlend",
    "Okalla",
    "Abessolo",
    "Ndongo",
    "Ewane",
    "Tchoumi",
    "Fouda",
    "Etoundi",
    "Kamdem",
    "Fotsing",
    "Nguemeni",
    "Yonta",
    "Ateba",
    "Song",
    "Kouam",
    "Biya",
    "Mebana",
    "Minko",
    "Talla",
    "Noubissie",
    "Essomba",
    "Motaze",
    "Ze",
    "Abena",
    "Nana",
    "Bekolo",
    "Kombi",
    "Manga",
    "Moue",
    "Likeng",
    "Mvondo",
    "Belinga",
    "Tchana",
    "Bam",
    "Ndjock",
    "Ngassa",
    "Soha",
    "Moussima",
    "Talla",
    "Kepseu",
    "Bopda",
    "Ngadeu",
    "Dassi",
    "Mekam",
    "Ndoumbe",
    "Nzima",
    "Fonyuy",
    "Kamga",
    "Bekima",
    "Ambassa",
    "Ngandjo",
    "Kuitche",
    "Nchout",
    "Nguefack",
    "Tchouadeu",
    "Siewe",
    "Fofe",
    "Mevoua",
    "Eyong",
    "Njike",
    "Tabi",
    "Ngole",
    "Dikom",
    "Etundi",
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
    "Flutter",
    "Laravel",
    "PowerBI",
    "Snowflake",
    "Comptabilité",
    "Gestion RH",
    "Service client",
    "Coiffure",
    "Cuisine professionnelle",
    "Entretien ménager",
    "Conduite moto",
    "Livraison urbaine",
    "Marketing terrain",
    "Gestion de caisse",
    "Relation client",
    "Sécurité privée",
    "Manucure",
    "Bricolage",
    "Logistique urbaine",
    "Gestion de stocks",
    "Soins infantiles",
    "Massothérapie",
    "Maintenance électroménager",
    "Scrum",
    "Communication",
    "Reporting",
    "Gestion boutique",
    "Conduite poids lourd",
    "Technicien froid",
]

PROJECT_TITLES = [
    "Plateforme RH Cameroun",
    "Portail E-commerce Douala",
    "Application mobile santé",
    "Solution IoT agricole",
    "Système de paiement mobile",
    "Tableau de bord logistique",
    "Programme d'alphabétisation",
    "Gestion des réservations hôtelières",
    "Application de livraison alimentaire",
    "Plateforme d'artisans locaux",
    "Outil de suivi RH",
    "Centre d'appel virtuel",
    "Projet solaire communautaire",
    "Atelier de couture collaborative",
    "Service de nounous connectées",
    "Réseau des salons de coiffure",
    "Application de gestion de caisse",
    "Portail de microcrédit",
    "Solution de nettoyage à la demande",
    "Projet d'agriculture urbaine",
    "Plateforme logistique pour livreurs",
    "Programme d'insertion ménagères",
    "Académie des barbiers",
    "Plateforme de recrutement RH",
    "Portail de réservation taxis-motos",
]

CANDIDATE_LANGUAGE_LEVELS = [
    LanguageLevel.A1,
    LanguageLevel.A2,
    LanguageLevel.B1,
    LanguageLevel.B2,
    LanguageLevel.C1,
    LanguageLevel.C2,
]

LANGUAGE_NAMES = [
    "Français",
    "Anglais",
    "Espagnol",
    "Allemand",
    "Arabe",
]


def _add_all(session: Session, items: Iterable[object]) -> None:
    for item in items:
        session.add(item)


def _email(first: str, last: str, suffix: str) -> str:
    slug = f"{first}.{last}".replace(" ", "").lower()
    return f"{slug}.{suffix}@example.com"


def _decimal_amount(amount: int) -> Decimal:
    return Decimal(str(amount))


def _build_job_catalog() -> list[dict]:
    catalog: list[dict] = []
    idx = 0
    while len(catalog) < 120:
        profile = JOB_PROFILES[idx % len(JOB_PROFILES)]
        country, city, _ = CAMEROON_LOCATIONS[idx % len(CAMEROON_LOCATIONS)]
        company = CAMEROON_COMPANIES[idx % len(CAMEROON_COMPANIES)]
        salary_min, salary_max = profile["salary_range"]
        catalog.append(
            {
                "title": profile["title"],
                "description": f"{profile['title']} pour {company} à {city}.",
                "mobility": profile["mobility"],
                "position_type": profile["position_type"],
                "seniority": profile["seniority"],
                "duration_months": random.choice([6, 12, 18]),
                "salary_min": _decimal_amount(salary_min + (idx % 4) * 100000),
                "salary_max": _decimal_amount(salary_max + (idx % 4) * 120000),
                "salary_avg": _decimal_amount((salary_min + salary_max) // 2),
                "salary_type": SalaryType.INTERVAL,
                "experience_years": random.randint(2, 6),
                "priority_level": random.randint(1, 10),
                "country": country,
                "city": city,
                "address": f"{random.randint(10, 150)} Avenue de l'Unité",
                "language": "fr",
                "skills": profile["skills"],
            }
        )
        idx += 1
    return catalog


JOB_CATALOG = _build_job_catalog()


def seed_candidates(db: Session, count: int = 48) -> list[tuple[User, Candidate]]:
    results: list[tuple[User, Candidate]] = []
    mobility_values = list(Mobility)
    notify_values = list(NotificationDelay)
    position_types = list(PositionType)
    levels = list(SeniorityLevel)

    for idx in range(count):
        first = CANDIDATE_FIRST_NAMES[idx % len(CANDIDATE_FIRST_NAMES)]
        last = CANDIDATE_LAST_NAMES[idx % len(CANDIDATE_LAST_NAMES)]
        country, city, _ = CAMEROON_LOCATIONS[idx % len(CAMEROON_LOCATIONS)]
        user = User(
            first_name=first,
            last_name=last,
            email=_email(first, last, f"cand{idx}"),
            phone=f"+2376{idx:02d}{idx+11:02d}{idx+22:02d}",
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.flush()

        base_salary = 2500000 + (idx % 6) * 150000
        candidate = Candidate(
            user_id=user.id,
            mobility=random.choice(mobility_values),
            country=country,
            city=city,
            address=f"{12+idx} Rue Nationale",
            salary_min=_decimal_amount(base_salary),
            salary_avg=_decimal_amount(base_salary + 250000),
            salary_max=_decimal_amount(base_salary + 500000),
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
            school=f"Université de {city}",
            description="Spécialité IA et cloud",
            start_date=date(2015 + (idx % 4), 9, 1),
            end_date=date(2017 + (idx % 4), 7, 1),
        )
        db.add(education)

        experience = Experience(
            candidate_id=candidate.id,
            title=random.choice(POSITION_TITLES),
            company=f"Startup {idx % 20 + 1} Cameroun",
            description="Contribution à des plateformes cloud locales.",
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
                    level=random.choice(CANDIDATE_LANGUAGE_LEVELS),
                )
                for lang in languages
            ),
        )

        results.append((user, candidate))

    return results


def seed_recruiters(
    db: Session,
    job_catalog: list[dict],
    count: int = 24,
) -> tuple[list[tuple[User, Recruiter]], int]:
    results: list[tuple[User, Recruiter]] = []
    job_index = 0
    offers_created = 0

    for idx in range(count):
        first = RECRUITER_FIRST_NAMES[idx % len(RECRUITER_FIRST_NAMES)]
        last = RECRUITER_LAST_NAMES[idx % len(RECRUITER_LAST_NAMES)]
        org = f"{CAMEROON_COMPANIES[idx % len(CAMEROON_COMPANIES)]} RH"
        user = User(
            first_name=first,
            last_name=last,
            email=_email(first, last, f"recr{idx}"),
            phone=f"+2372{idx:02d}{idx+33:02d}{idx+55:02d}",
            role=UserRole.RECRUITER,
        )
        db.add(user)
        db.flush()

        recruiter = Recruiter(user_id=user.id, organization_name=org)
        db.add(recruiter)
        db.flush()

        template_job = job_catalog[idx % len(job_catalog)]
        template = OfferTemplate(
            recruiter_id=recruiter.id,
            title=f"Modèle {template_job['title']}",
            description=f"Modèle pour les postes {template_job['title']} au Cameroun.",
            mobility=template_job["mobility"],
            position_type=template_job["position_type"],
            seniority=template_job["seniority"],
            duration_months=template_job["duration_months"],
            salary_min=template_job["salary_min"],
            salary_max=template_job["salary_max"],
            salary_avg=template_job["salary_avg"],
            salary_type=template_job["salary_type"],
            experience_years=template_job["experience_years"],
            priority_level=template_job["priority_level"],
            country=template_job["country"],
            city=template_job["city"],
            address=template_job["address"],
            language="fr",
        )
        db.add(template)
        db.flush()

        _add_all(
            db,
            (OfferSkill(template_id=template.id, title=skill) for skill in template_job["skills"]),
        )

        offers_to_create = 5
        for _ in range(offers_to_create):
            if job_index >= len(job_catalog):
                break
            job = job_catalog[job_index]
            job_index += 1
            offer = Offer(
                recruiter_id=recruiter.id,
                template_id=template.id,
                title=job["title"],
                description=job["description"],
                mobility=job["mobility"],
                position_type=job["position_type"],
                seniority=job["seniority"],
                duration_months=job["duration_months"],
                salary_min=job["salary_min"],
                salary_max=job["salary_max"],
                salary_avg=job["salary_avg"],
                salary_type=job["salary_type"],
                experience_years=job["experience_years"],
                priority_level=job["priority_level"],
                country=job["country"],
                city=job["city"],
                address=job["address"],
                language=job["language"],
            )
            db.add(offer)
            db.flush()
            offers_created += 1

            _add_all(
                db,
                (OfferSkill(offer_id=offer.id, title=skill) for skill in job["skills"]),
            )

        results.append((user, recruiter))

    return results, offers_created


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
    recruiter_searches = max(20, len(recruiter_profiles) // 2)
    for idx in range(recruiter_searches):
        rec_user, _ = recruiter_profiles[idx % len(recruiter_profiles)]
        country, city, _ = CAMEROON_LOCATIONS[idx % len(CAMEROON_LOCATIONS)]
        searches.append(
            Search(
                user_id=rec_user.id,
                query="Talents développeurs Cameroun",
                type=SearchType.DEFAULT,
                target=SearchTarget.CANDIDATE,
                country=country,
                city=city,
                contract_type=PositionType.CDI,
                language="fr",
            )
        )
    _add_all(db, searches)

    # Recommendations
    recommendations = []
    for idx in range(30):
        rec_user, _ = recruiter_profiles[idx % len(recruiter_profiles)]
        cand_user, _ = candidate_profiles[idx % len(candidate_profiles)]
        recommendations.append(
            Recommendation(
                label=f"Candidat recommandé : {cand_user.first_name}",
                target=RecommendationTarget.CANDIDATE,
                user_id=rec_user.id,
                number=random.randint(1, 5),
            )
        )
        recommendations.append(
            Recommendation(
                label=f"Recruteur fiable : {rec_user.first_name}",
                target=RecommendationTarget.RECRUITER,
                user_id=cand_user.id,
                number=random.randint(1, 5),
            )
        )
    _add_all(db, recommendations)

    # Chats & messages (30 pairs)
    chat_pairs = 30
    for idx in range(chat_pairs):
        cand_user, _ = candidate_profiles[idx % len(candidate_profiles)]
        rec_user, _ = recruiter_profiles[idx % len(recruiter_profiles)]
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
                content=f"Bonjour {rec_user.first_name}, intéressé par l'offre {idx+1}.",
            ),
            Message(
                session_id=chat.id,
                sender_id=rec_user.id,
                receiver_id=cand_user.id,
                content="Merci pour votre intérêt, partagez vos disponibilités.",
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

        logger.info("Seeding %s candidates (Cameroun)", 48)
        candidate_profiles = seed_candidates(db, count=48)

        logger.info("Seeding recruiters and offers (Cameroun)")
        recruiter_profiles, offers_created = seed_recruiters(
            db,
            job_catalog=JOB_CATALOG,
            count=24,
        )
        if offers_created < 100:
            logger.warning(
                "Only %s offers created; consider increasing job catalog or recruiter count.",
                offers_created,
            )

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
