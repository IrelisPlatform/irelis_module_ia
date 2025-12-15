from __future__ import annotations

import random
from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import (
    Application,
    ApplicationDocument,
    Candidate,
    CandidatureInfo,
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
    RequiredDocument,
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
)

random.seed(42)

CAMEROON_CITIES = {
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
    "Kribi": "Sud",
    "Bertoua": "Est",
}

CAMEROON_COMPANIES = [
    "Société Industrielle du Littoral",
    "Banque Atlantique Cameroun",
    "Cameroon Cocoa Export",
    "Douala Tech Hub",
    "Energie Verte Cameroun",
    "Sahel Agro Services",
    "Littoral Maritime Logistics",
    "Atlas Assurance Cameroun",
    "Camer Fibre Optique",
    "Cité Financière Yaoundé",
    "Cameroon HealthCare Systems",
    "Nord Sud Consulting",
    "Innovation Douala Port",
    "Kmer Design Studio",
    "Alliance Agroforestière",
    "Cameroon Food Lab",
    "Horizon Telecom Network",
    "Cameroon Digital Factory",
    "Kribi Marine Services",
    "Africa Data Mining",
    "Yaoundé Business Angels",
    "Douala Fintech Capital",
    "Cameroon Agritech Labs",
    "Kribi Shipping Agency",
    "Sawa Engineering Works",
    "Central Cloud Africa",
    "Garoua Smart Farming",
    "Ekollo Medical Group",
    "Cameroon Clean Energy",
    "Douala Talent Studio",
    "Cameroon Mobility Tech",
    "Ocean Services Cameroun",
    "Buea Creative Agency",
    "Makossa Media Lab",
    "Cameroon Steel & Build",
    "Savannah Security Labs",
    "Cameroon Digital Rail",
    "Yaoundé Civic Services",
    "Bamenda Software Studio",
    "Cameroon Green Mobility",
    "Douala Commerce Connect",
    "Yaoundé Agro Sciences",
    "Cameroon Space Systems",
    "Kribi Innovation Port",
    "Seme Beach Resorts",
    "Cameroon Rural Tech",
    "Douala Cloud Retail",
    "Cameroon Smart Supply",
    "Sahel Medical Devices",
    "Cameroon Textile Works",
]

JOB_TITLES = [
    "Ingénieur DevOps",
    "Chargé de Marketing Digital",
    "Consultant Cybersécurité",
    "Analyste Financier",
    "Community Manager",
    "Responsable RH",
    "Architecte Cloud",
    "Développeur Mobile",
    "Ingénieur Logiciel",
    "Data Engineer",
    "Machine Learning Engineer",
    "Chef de Projet IT",
    "Responsable Produit",
    "Scrum Master",
    "Ingénieur QA",
    "Responsable Infrastructure",
    "Analyste Données",
    "Technicien Support",
    "Ingénieur Réseaux",
    "Coach Agile",
    "Designer UX/UI",
    "Consultant Cloud",
    "Responsable Logistique",
    "Analyste Risques",
    "Responsable Conformité",
    "Ingénieur Sécurité",
    "Responsable Innovation",
    "Data Scientist",
    "Full Stack Developer",
]

CANDIDATE_FIRST_NAMES = [
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
    "Leandre",
    "Rosine",
    "David",
    "Celestine",
    "Franck",
    "Nathalie",
    "Sylvain",
    "Grace",
    "Hervé",
    "Claudine",
    "Joel",
    "Arlette",
    "Vivien",
    "Clarisse",
]

CANDIDATE_LAST_NAMES = [
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
    "Nkoa",
    "Djoumessi",
    "Mendouga",
    "Ngono",
    "Essomba",
    "Fokou",
    "Manga",
    "Biloa",
    "Nanfack",
    "Mouelle",
    "Kemgne",
    "Nzie",
    "Ngalle",
    "Tchounga",
]

EDUCATION_DEGREES = [
    "Licence en Génie Logiciel",
    "Master en Management",
    "Licence en Communication",
    "Master en Finance",
    "Licence en Réseaux",
    "Master en Data Science",
    "Diplôme en Commerce International",
]

EXPERIENCE_POSITIONS = [
    "Assistant Technique",
    "Chargé de Production",
    "Analyste Junior",
    "Chef de Service",
    "Coordonnateur Terrain",
    "Ingénieur de Tests",
    "Consultant Fonctionnel",
]

SKILL_TOPICS = [
    "Python",
    "Django",
    "FastAPI",
    "TypeScript",
    "React",
    "Azure",
    "Kubernetes",
    "Scrum",
    "Leadership",
    "Marketing digital",
    "Analyse financière",
    "Communication",
    "Docker",
    "Terraform",
    "Power BI",
    "TensorFlow",
    "NLP",
    "Penetration testing",
    "Network security",
    "ERP",
    "CRM",
    "Copywriting",
    "SEO",
    "DevOps",
    "Microservices",
    "Angular",
    "Vue.js",
    "Flutter",
    "Node.js",
    "Java",
    "Spring Boot",
    "Kotlin",
    "Data viz",
    "Agilité",
    "Product discovery",
    "Gestion de produit",
    "Expérience utilisateur",
    "Cloud hybride",
    "Support technique",
]

LANGUAGES = ["Français", "Anglais"]

SECTOR_ENTRIES = [
    ("Technologie du Littoral", "Solutions cloud et télécoms"),
    ("Agro Business Centre", "Chaînes d'approvisionnement agricoles"),
    ("Énergie Verte Sahel", "Production solaire et éolienne"),
    ("Finance Inclusive", "Microfinance et fintech"),
    ("Santé Horizon", "Centres hospitaliers privés"),
    ("Transport Urbain Cameroun", "Logistique urbaine"),
    ("Tourisme Kribi", "Hôtellerie et loisirs"),
    ("Construction Nord", "BTP et ouvrages publics"),
    ("Télécoms Sud", "Réseaux mobiles et data"),
    ("Média Digital", "Studios et plateformes médias"),
    ("Commerce Douala Port", "Import-export maritime"),
    ("Éducation Connectée", "Formation en ligne"),
    ("Industrie Agroalimentaire", "Transformation alimentaire"),
    ("Services Juridiques", "Cabinets d'avocats"),
    ("Mode & Textile", "Créateurs locaux"),
    ("Finance Durable", "Investissements verts"),
    ("Sécurité Numérique", "Opérations SOC"),
    ("Sport & Bien-être", "Centres fitness"),
    ("Mobilité Verte", "Solutions de transport propres"),
    ("Gestion de Patrimoine", "Conseil financier"),
    ("Innovation Sociale", "Incubateurs d'impact"),
    ("Logistique Pétrolière", "Services offshore"),
    ("Hydraulique Cameroun", "Traitement d'eau"),
    ("Biotech Tropique", "Laboratoires pharmaceutiques"),
    ("Agriculture Intelligente", "IoT agricole"),
    ("Restauration Premium", "Chaînes culinaires"),
    ("Immobilier Urbain", "Promotion immobilière"),
    ("Art & Culture", "Studios créatifs"),
    ("Services Publics", "Modernisation des administrations"),
    ("Cybersécurité Nationale", "Protection des infrastructures"),
    ("Banque Digitale", "Services bancaires mobiles"),
]


def clear_tables(db: Session) -> None:
    """Truncate or delete existing data to reset the database."""
    models = [
        JobOfferTag,
        RequiredDocument,
        CandidatureInfo,
        SavedJobOffer,
        ApplicationDocument,
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
    """Insert demo sectors and return them."""
    sectors: list[Sector] = []
    for name, description in SECTOR_ENTRIES:
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
    """Insert base tags used throughout the system."""
    tags: list[Tag] = []
    for skill in SKILL_TOPICS:
        tag = Tag(
            name=skill,
            type="SKILL",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(tag)
        tags.append(tag)
    db.flush()
    return tags


def create_recruiters(db: Session, sectors: list[Sector]) -> tuple[list[Recruiter], list[User]]:
    """Create recruiters and associated users for seeding."""
    recruiters: list[Recruiter] = []
    recruiter_users: list[User] = []
    for i in range(52):
        company = CAMEROON_COMPANIES[i % len(CAMEROON_COMPANIES)]
        city = random.choice(list(CAMEROON_CITIES.keys()))

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

        recruiter = Recruiter(
            company_description=f"{company} accompagne les entreprises camerounaises.",
            company_email=f"contact@{company.lower().replace(' ', '')}.cm",
            company_length=random.randint(25, 500),
            company_linked_in_url=f"https://www.linkedin.com/company/{company.lower().replace(' ', '')}",
            company_logo_url="https://placeholder.com/logo.png",
            company_name=company,
            company_phone=f"+2376{random.randint(10000000, 99999999)}",
            company_website=f"https://{company.lower().replace(' ', '')}.cm",
            first_name=random.choice(CANDIDATE_FIRST_NAMES),
            function="Directeur des Ressources Humaines",
            last_name=random.choice(CANDIDATE_LAST_NAMES),
            city=city,
            country="Cameroon",
            region=CAMEROON_CITIES[city],
            phone_number=f"+2376{random.randint(10000000, 99999999)}",
            sector_id=random.choice(sectors).id,
            user_id=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(recruiter)
        recruiters.append(recruiter)
        recruiter_users.append(user)
    db.flush()
    return recruiters, recruiter_users


def create_job_offers(db: Session, recruiters: list[Recruiter], tags: list[Tag]) -> list[JobOffer]:
    """Insert sample job offers owned by seeded recruiters."""
    offers: list[JobOffer] = []
    for recruiter in recruiters:
        for _ in range(random.randint(2, 4)):
            city = random.choice(list(CAMEROON_CITIES.keys()))
            min_salary = random.randint(250_000, 600_000)
            max_salary = min_salary + random.randint(100_000, 450_000)
            language = random.choice(LANGUAGES)
            job = JobOffer(
                contract_type=random.choice(list(ContractType)),
                description=f"{recruiter.company_name} recrute un {random.choice(JOB_TITLES)} basé à {city}.",
                expiration_date=datetime.utcnow() + timedelta(days=random.randint(30, 120)),
                instructions="Envoyez votre dossier complet via le portail entreprise.",
                is_featured=random.choice([True, False]),
                is_urgent=random.choice([True, False]),
                job_type=random.choice(list(JobType)),
                post_number=random.randint(1, 5),
                published_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                required_language=language,
                salary=f"{min_salary} - {max_salary} XAF",
                status=random.choice(list(JobOfferStatus)),
                title=random.choice(JOB_TITLES),
                work_city_location=city,
                work_country_location="Cameroon",
                company_id=recruiter.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            skill_choices = random.sample(tags, k=min(3, len(tags)))
            job.tags.extend(skill_choices)
            db.add(job)
            offers.append(job)

            candidature = CandidatureInfo(
                job_offer=job,
                email_candidature=f"jobs@{recruiter.company_name.lower().replace(' ', '')}.cm",
                instructions="CV, lettre de motivation et références requises.",
                required_documents="CV, COVER_LETTER",
                url_candidature=f"https://jobs.{recruiter.company_name.lower().replace(' ', '')}.cm/apply",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(candidature)

            required_types = random.sample(list(DocumentType), k=2)
            for doc_type in required_types:
                requirement = RequiredDocument(
                    job_offer=job,
                    type=doc_type,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                db.add(requirement)
    db.flush()
    return offers


def create_candidates(db: Session, sectors: list[Sector]) -> tuple[list[Candidate], list[User]]:
    """Create candidate profiles (with related entities) and back their users."""
    candidates: list[Candidate] = []
    candidate_users: list[User] = []
    for i in range(60):
        first = CANDIDATE_FIRST_NAMES[i % len(CANDIDATE_FIRST_NAMES)]
        last = CANDIDATE_LAST_NAMES[i % len(CANDIDATE_LAST_NAMES)]
        city = random.choice(list(CAMEROON_CITIES.keys()))

        user = User(
            email=f"{first.lower()}.{last.lower()}{i+1}@candidates.cm",
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

        candidate = Candidate(
            avatar_url="https://placeholder.com/avatar.png",
            birth_date=datetime.utcnow() - timedelta(days=random.randint(8000, 15000)),
            completion_rate=round(random.uniform(65, 98), 2),
            experience_level=random.choice(list(ExperienceLevel)).value,
            first_name=first,
            last_name=last,
            city=city,
            country="Cameroon",
            region=CAMEROON_CITIES[city],
            last_viewed_month=datetime.utcnow().replace(day=1),
            monthly_profile_views=random.randint(40, 200),
            profile_views=random.randint(200, 2500),
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
        candidate_users.append(user)
        db.flush()

        job_pref = JobPreferences(
            availability=random.choice(["Disponible", "Préavis 1 mois", "Préavis 2 mois"]),
            desired_position=random.choice(JOB_TITLES),
            city=candidate.city,
            country="Cameroon",
            region=candidate.region,
            pretentions_salarial=f"{random.randint(300000, 700000)} XAF",
            candidate_id=candidate.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(job_pref)
        db.flush()

        for contract_type in random.sample(list(ContractType), k=2):
            db.add(
                JobPreferencesContractType(
                    job_preferences_id=job_pref.id,
                    contract_type=contract_type,
                )
            )

        for sector in random.sample(sectors, k=2):
            db.add(
                JobPreferencesSector(
                    job_preferences_id=job_pref.id,
                    sector_id=sector.id,
                )
            )

        edu_count = random.randint(2, 3)
        for _ in range(edu_count):
            db.add(
                Education(
                    city=candidate.city,
                    degree=random.choice(EDUCATION_DEGREES),
                    graduation_year=random.randint(2010, 2024),
                    institution=f"Université de {candidate.city}",
                    candidate_id=candidate.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
            )

        exp_count = random.randint(1, 2)
        for _ in range(exp_count):
            db.add(
                Experience(
                    city=candidate.city,
                    company_name=random.choice(CAMEROON_COMPANIES),
                    description="Participation à des projets nationaux à fort impact.",
                    end_date=datetime.utcnow(),
                    is_current=random.choice([True, False]),
                    position=random.choice(EXPERIENCE_POSITIONS),
                    start_date=datetime.utcnow() - timedelta(days=random.randint(400, 1500)),
                    candidate_id=candidate.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
            )

        for _ in range(3):
            db.add(
                Skill(
                    level=random.choice(list(SkillLevel)),
                    name=random.choice(SKILL_TOPICS),
                    candidate_id=candidate.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
            )

        for _ in range(2):
            db.add(
                Language(
                    language=random.choice(LANGUAGES),
                    level=random.choice(list(LanguageLevel)),
                    candidate_id=candidate.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
            )
    db.flush()
    return candidates, candidate_users


def create_applications_and_documents(
    db: Session,
    candidates: list[Candidate],
    job_offers: list[JobOffer],
) -> None:
    """Seed demo applications, documents, and saved offers."""
    applications: list[Application] = []
    for _ in range(80):
        application = Application(
            candidate_id=random.choice(candidates).id,
            job_offer_id=random.choice(job_offers).id,
            applied_at=datetime.utcnow() - timedelta(days=random.randint(0, 45)),
            message="Veuillez trouver ci-joint mon CV et ma lettre de motivation.",
            status=random.choice(list(ApplicationStatus)),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(application)
        applications.append(application)
    db.flush()

    for application in applications:
        doc_types = random.sample(list(DocumentType), k=2)
        for doc_type in doc_types:
            db.add(
                ApplicationDocument(
                    application_id=application.id,
                    storage_url=f"https://cdn.irelis.cm/docs/{application.id}/{doc_type.value.lower()}.pdf",
                    type=doc_type,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
            )

    for _ in range(60):
        db.add(
            SavedJobOffer(
                candidate_id=random.choice(candidates).id,
                job_offer_id=random.choice(job_offers).id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
    db.flush()


def create_email_otps(db: Session, users: list[User]) -> None:
    """Create OTP entries for random users."""
    for _ in range(40):
        user = random.choice(users)
        otp = EmailOtp(
            code=str(random.randint(100000, 999999)),
            consumed=random.choice([True, False]),
            email=user.email,
            expires_at=datetime.utcnow() + timedelta(minutes=20),
            purpose=random.choice(list(OtpPurpose)),
            user_type=user.user_type or UserType.CANDIDATE,
        )
        db.add(otp)
    db.flush()


def create_sessions(db: Session, users: list[User]) -> None:
    """Create active sessions for a subset of users."""
    selected = random.sample(users, k=min(60, len(users)))
    for user in selected:
        session = UserSession(
            device_info="app-mobile",
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
    """High-level seeding routine used by CLI."""
    db = SessionLocal()
    try:
        clear_tables(db)
        sectors = create_sectors(db)
        tags = create_tags(db)
        recruiters, recruiter_users = create_recruiters(db, sectors)
        job_offers = create_job_offers(db, recruiters, tags)
        candidates, candidate_users = create_candidates(db, sectors)
        create_applications_and_documents(db, candidates, job_offers)
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
