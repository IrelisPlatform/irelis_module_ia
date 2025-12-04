from __future__ import annotations

import random
from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import (
    Application,
    Candidate,
    Education,
    EmailOtp,
    Experience,
    JobOffer,
    JobOfferTag,
    JobPreferences,
    JobPreferencesContractType,
    JobPreferencesSector,
    Language,
    Recruiter,
    SavedJobOffer,
    Sector,
    Skill,
    Tag,
    User,
    UserSession,
)
from app.models.enums import (
    ApplicationStatus,
    ContractType,
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
)

random.seed(42)

CITY_REGION = {
    "Douala": "Littoral",
    "Yaoundé": "Centre",
    "Bafoussam": "Ouest",
    "Buea": "Sud-Ouest",
    "Limbe": "Littoral",
    "Maroua": "Extrême-Nord",
    "Ngaoundéré": "Adamaoua",
    "Ebolowa": "Sud",
    "Garoua": "Nord",
    "Bamenda": "Nord-Ouest",
}

CAMEROON_COMPANIES = [
    "Société Industrielle du Littoral",
    "Groupe Agro Alimentaire CMR",
    "Télécoms du Grand Ouest",
    "Finances et Services Africains",
    "Campus Tech Cameroon",
    "Énergies Vertes du Centre",
    "Solutions Logistiques Afrique",
    "Bank of Sahel Mauve",
    "Immobilier Douala City",
    "Transport Express Yaoundé",
    "Douala Cloud Services",
    "Yaoundé Digital Factory",
    "Kamer Cyber Security Labs",
    "NorthTech Cameroon",
    "DeepData Analytics CM",
    "SmartGrid Cameroon",
    "AI Solutions Sahel",
    "GreenIT Yaoundé",
    "HealthTech Douala",
    "Fintech Kmer Connect",
    "EduTech Horizon",
    "CryptoPay Central Africa",
]

JOB_TITLES = [
    "Ingénieur DevOps",
    "Responsable Recrutement",
    "Chargé de Marketing Digital",
    "Consultant en Transformation",
    "Analyste Financier",
    "Chef de Projet Infrastructure",
    "Technicien Support",
    "Directeur des Opérations",
    "Community Manager",
    "Responsable Qualité",
    "Chargé de Compte",
    "Planificateur Supply Chain",
    "UX/UI Designer",
    "Technicien Sécurité",
    "Coordinateur RH",
    "Architecte Cloud",
    "Développeur Mobile",
    "Ingénieur Logiciel Senior",
    "Responsable Produit IT",
    "Analyste Données",
    "Consultant Cybersécurité",
    "Scrum Master",
    "Ingénieur QA Automation",
    "Data Engineer",
    "Machine Learning Engineer",
    "Responsable ITSM",
]

CAMEROON_CANDIDATE_FIRST = [
    "Alice",
    "Samuel",
    "Jacqueline",
    "Michel",
    "Florence",
    "Emmanuel",
    "Nadine",
    "Patrick",
    "Christine",
    "Boris",
    "Yvonne",
    "Marc",
    "Estelle",
    "Adolphe",
    "Sandrine",
    "Jean",
    "Ariane",
    "Léandre",
    "Rosine",
    "David",
    "Célestine",
    "Franck",
    "Nathalie",
]

CAMEROON_CANDIDATE_LAST = [
    "Ndongo",
    "Nkeng",
    "Mbang",
    "Kemayou",
    "Kouam",
    "Tamekou",
    "Dounia",
    "Tsafack",
    "Atangana",
    "Nnanga",
    "Eyoum",
    "Tsala",
    "Mouafo",
    "Mba",
    "Nguim",
    "Ncho",
]

EDUCATION_DEGREES = [
    "Licence en Génie Logiciel",
    "Master en Management des Entreprises",
    "Diplôme en Administration Industrielle",
    "Licence en Communication",
    "Master en Finance",
    "Licence en Sciences Informatiques",
]

EXPERIENCE_POSITIONS = [
    "Assistant Technique",
    "Chargé de Production",
    "Analyste Junior",
    "Chef de Service",
    "Coordonnateur Terrain",
]

SKILL_NAMES = [
    "Leadership",
    "Gestion de projet",
    "Python",
    "SQL",
    "Marketing digital",
    "Analyse financière",
    "Communication",
    "Gestion des partenariats",
    "Django",
    "Flask",
    "FastAPI",
    "TypeScript",
    "React",
    "Vue.js",
    "Angular",
    "Node.js",
    "Java",
    "Spring Boot",
    "Kotlin",
    "Swift",
    "Flutter",
    "Kubernetes",
    "Docker",
    "Terraform",
    "AWS",
    "Azure",
    "GCP",
    "CI/CD",
    "Power BI",
    "Data visualization",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "Computer vision",
    "Penetration testing",
    "Network security",
    "ERP",
    "CRM",
    "Scrum",
    "Kanban",
    "Product discovery",
    "Copywriting",
    "SEO",
    "SEA",
]

LANGUAGES = ["Français", "Anglais"]

TAGS = [
    "management",
    "digital",
    "énergie",
    "banque",
    "agroalimentaire",
    "transport",
    "santé",
    "éducation",
    "génie logiciel",
    "logistique",
    "service client",
    "comptable",
    "commerce international",
    "recrutement",
    "cybersécurité",
    "cloud",
    "devops",
    "data science",
    "big data",
    "intelligence artificielle",
    "iot",
    "robotique",
    "blockchain",
    "fintech",
    "edtech",
    "healthtech",
    "cleantech",
    "sécurité réseau",
    "microservices",
    "api",
    "testing",
    "agilité",
    "scrum",
    "gestion de produit",
    "expérience utilisateur",
    "design system",
    "animation 3d",
    "réalité augmentée",
    "réalité virtuelle",
    "cloud hybride",
    "infrastructure",
    "bureautique",
    "commerce électronique",
    "support technique",
    "innovation",
    "veille technologique",
    "communication interne",
]

def clear_tables(db: Session) -> None:
    models = [
        JobOfferTag,
        SavedJobOffer,
        Application,
        JobPreferencesSector,
        JobPreferencesContractType,
        JobPreferences,
        JobOffer,
        Recruiter,
        Education,
        Experience,
        Skill,
        Language,
        Candidate,
        Sector,
        Tag,
        EmailOtp,
        UserSession,
        User,
    ]
    for model in models:
        db.execute(delete(model))
    db.commit()


def create_sectors(db: Session) -> list[Sector]:
    sectors: list[Sector] = []
    for name, description in [
        ("Technologie", "Solutions numériques et services"),
        ("Agriculture", "Agro-industrie et chaînes d'approvisionnement"),
        ("Finance", "Banques et assurances"),
        ("Énergies", "Production et distribution"),
        ("Santé", "Services hospitaliers et cliniques"),
        ("Logistique", "Transport de marchandises"),
        ("Éducation", "Institutions et formation"),
        ("Télécommunications", "Réseaux mobiles et fixes"),
        ("Tourisme", "Hôtellerie et événements"),
    ]:
        sector = Sector(
            name=name,
            description=description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(sector)
        sectors.append(sector)
    db.flush()
    return sectors


def create_tags(db: Session) -> list[Tag]:
    tags: list[Tag] = []
    for nom in TAGS:
        tag = Tag(nom=nom)
        db.add(tag)
        tags.append(tag)
    db.flush()
    return tags


def create_recruiters(db: Session, sectors: list[Sector]) -> tuple[list[Recruiter], list[User]]:
    recruiters: list[Recruiter] = []
    users: list[User] = []
    for i in range(60):
        company = CAMEROON_COMPANIES[i % len(CAMEROON_COMPANIES)]
        user = User(
            email=f"recruteur{i+1}@{company.lower().replace(' ', '')}.cm",
            password="SecurePass123!",
            provider=Provider.EMAIL,
            role=UserRole.RECRUITER,
            user_type=UserType.RECRUITER,
            deleted=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(user)
        db.flush()

        city = random.choice(list(CITY_REGION.keys()))
        recruiter = Recruiter(
            company_description=f"{company} est un acteur clé au Cameroun.",
            company_email=f"contact@{company.lower().replace(' ', '')}.cm",
            company_length=random.randint(20, 500),
            company_linked_in_url=f"https://www.linkedin.com/company/{company.lower().replace(' ', '')}",
            company_logo_url="https://placeholder.com/logo.png",
            company_name=f"{company} {i+1}",
            company_phone=f"+2376{random.randint(10000000, 99999999)}",
            company_website=f"https://{company.lower().replace(' ', '')}.cm",
            first_name=random.choice(CAMEROON_CANDIDATE_FIRST),
            function="Directeur des Ressources Humaines",
            last_name=random.choice(CAMEROON_CANDIDATE_LAST),
            city=city,
            country="Cameroon",
            region=CITY_REGION[city],
            phone_number=f"+2376{random.randint(10000000, 99999999)}",
            sector_id=random.choice(sectors).id,
            user_id=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(recruiter)
        recruiters.append(recruiter)
        users.append(user)
    db.flush()
    return recruiters, users


def create_job_offers(db: Session, recruiters: list[Recruiter], tags: list[Tag]) -> list[JobOffer]:
    job_offers: list[JobOffer] = []
    for recruiter in recruiters:
        for _ in range(random.randint(1, 5)):
            city = random.choice(list(CITY_REGION.keys()))
            min_salary = random.randint(200000, 500000)
            max_salary = min_salary + random.randint(80000, 400000)
            offer = JobOffer(
                contract_type=random.choice(list(ContractType)),
                description=f"Nous recherchons un(e) {random.choice(JOB_TITLES)} pour renforcer les équipes au Cameroun.",
                experience_level=random.choice(list(ExperienceLevel)),
                expiration_date=datetime.utcnow() + timedelta(days=random.randint(30, 120)),
                is_featured=random.choice([True, False]),
                is_urgent=random.choice([False, True]),
                job_type=random.choice(list(JobType)),
                city=city,
                country="Cameroon",
                region=CITY_REGION[city],
                max_salary=float(max_salary),
                min_salary=float(min_salary),
                published_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                school_level=random.choice(list(SchoolLevel)),
                show_salary=True,
                status=random.choice(list(JobOfferStatus)),
                title=random.choice(JOB_TITLES),
                company_id=recruiter.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            selected_tags = random.sample(tags, k=random.randint(1, 3))
            offer.tags.extend(selected_tags)
            db.add(offer)
            job_offers.append(offer)
    db.flush()
    return job_offers


def create_candidates(db: Session, sectors: list[Sector]) -> tuple[list[Candidate], list[User]]:
    candidates: list[Candidate] = []
    users: list[User] = []
    for i in range(44):
        first_name = CAMEROON_CANDIDATE_FIRST[i % len(CAMEROON_CANDIDATE_FIRST)]
        last_name = CAMEROON_CANDIDATE_LAST[i % len(CAMEROON_CANDIDATE_LAST)]
        user = User(
            email=f"{first_name.lower()}.{last_name.lower()}{i+1}@candidates.cm",
            password="CandidatePass!2024",
            provider=Provider.EMAIL,
            role=UserRole.CANDIDATE,
            user_type=UserType.CANDIDATE,
            deleted=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(user)
        db.flush()

        city = random.choice(list(CITY_REGION.keys()))
        candidate = Candidate(
            avatar_url="https://placeholder.com/avatar.png",
            birth_date=datetime.utcnow() - timedelta(days=random.randint(8000, 15000)),
            completion_rate=round(random.uniform(65, 95), 2),
            experience_level=random.choice(list(ExperienceLevel)).value,
            first_name=first_name,
            last_name=last_name,
            city=city,
            country="Cameroon",
            region=CITY_REGION[city],
            phone_number=f"+2376{random.randint(10000000, 99999999)}",
            professional_title=random.choice(JOB_TITLES),
            school_level=random.choice(list(SchoolLevel)),
            user_id=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_visible=True,
        )
        db.add(candidate)
        candidates.append(candidate)
        users.append(user)
    db.flush()

    for candidate in candidates:
        job_pref = JobPreferences(
            availability=random.choice(["Disponible", "Préavis 1 mois", "Disponible immédiatement"]),
            desired_position=random.choice(JOB_TITLES),
            city=candidate.city,
            country="Cameroon",
            region=candidate.region,
            pretentions_salarial=f"{random.randint(250000, 600000)} XAF",
            candidate_id=candidate.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(job_pref)
        db.flush()
        contract_types = random.sample(list(ContractType), k=2)
        for contract_type in contract_types:
            contract_link = JobPreferencesContractType(
                job_preferences_id=job_pref.id,
                contract_type=contract_type,
            )
            db.add(contract_link)
        for sector_choice in random.sample(sectors, k=2):
            sector_link = JobPreferencesSector(
                job_preferences_id=job_pref.id,
                sector_id=sector_choice.id,
            )
            db.add(sector_link)

        for _ in range(random.randint(1, 2)):
            education = Education(
                city=candidate.city,
                degree=random.choice(EDUCATION_DEGREES),
                graduation_year=random.randint(2010, 2024),
                institution=f"Université de {candidate.city}",
                candidate_id=candidate.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(education)

        experience = Experience(
            city=candidate.city,
            company_name=random.choice(CAMEROON_COMPANIES),
            description="Contribué aux objectifs nationaux avec rigueur.",
            end_date=datetime.utcnow(),
            is_current=True,
            position=random.choice(EXPERIENCE_POSITIONS),
            start_date=datetime.utcnow() - timedelta(days=random.randint(300, 1200)),
            candidate_id=candidate.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(experience)

        for _ in range(2):
            skill = Skill(
                level=random.choice(list(SkillLevel)),
                name=random.choice(SKILL_NAMES),
                candidate_id=candidate.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(skill)

        language = Language(
            language=random.choice(LANGUAGES),
            level=random.choice(list(LanguageLevel)),
            candidate_id=candidate.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(language)

    db.flush()
    return candidates, users


def create_interactions(
    db: Session,
    candidates: list[Candidate],
    job_offers: list[JobOffer],
) -> None:
    for _ in range(30):
        application = Application(
            candidate_id=random.choice(candidates).id,
            job_offer_id=random.choice(job_offers).id,
            applied_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            status=random.choice(list(ApplicationStatus)),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(application)

    for _ in range(30):
        saved = SavedJobOffer(
            candidate_id=random.choice(candidates).id,
            job_offer_id=random.choice(job_offers).id,
            saved_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(saved)
    db.flush()


def create_email_otps(db: Session, users: list[User]) -> None:
    for _ in range(30):
        user = random.choice(users)
        otp = EmailOtp(
            code=str(random.randint(100000, 999999)),
            consumed=False,
            email=user.email,
            expires_at=datetime.utcnow() + timedelta(minutes=15),
            purpose=OtpPurpose.LOGIN_REGISTER,
            user_type=user.user_type if user.user_type is not None else UserType.CANDIDATE,
        )
        db.add(otp)
    db.flush()


def create_sessions(db: Session, users: list[User]) -> None:
    samples = random.sample(users, k=min(30, len(users)))
    for user in samples:
        session = UserSession(
            device_info="Naveau appareil mobile",
            expired_at=datetime.utcnow() + timedelta(days=7),
            ip_address=f"197.155.{random.randint(0,255)}.{random.randint(0,255)}",
            is_active=True,
            token=f"session-{user.id}",
            user_id=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(session)
    db.flush()


def seed_database() -> None:
    db = SessionLocal()
    try:
        clear_tables(db)
        sectors = create_sectors(db)
        tags = create_tags(db)
        recruiters, recruiter_users = create_recruiters(db, sectors)
        job_offers = create_job_offers(db, recruiters, tags)
        candidates, candidate_users = create_candidates(db, sectors)
        create_interactions(db, candidates, job_offers)
        create_email_otps(db, recruiter_users + candidate_users)
        create_sessions(db, recruiter_users + candidate_users)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
