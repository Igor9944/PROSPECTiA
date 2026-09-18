from datetime import datetime, timedelta, timezone

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import Activity, AIEvaluation, Company, Contact, Conversion, FollowUp, Prospect, User
from app.services.qualification import qualify_prospect

COMPANIES = [
    ("Apex Industrie", "Industrie", "Lyon", "France", 120, "https://apex-industrie.example", "Maintenance prédictive et ERP."),
    ("Santé Plus", "Santé", "Paris", "France", 340, "https://santeplus.example", "Groupe de cliniques, dossier patient et cybersécurité."),
    ("Nova Retail", "Commerce", "Lille", "France", 85, "https://novaretail.example", "Chaîne de magasins, unification des stocks."),
    ("Financia Conseil", "Finance", "Paris", "France", 60, "https://financia.example", "Cabinet, besoin de GED et MFA."),
    ("TransOcéan", "Transport", "Marseille", "France", 210, "https://transocean.example", "Flotte et TMS à moderniser."),
    ("Énergie Verte", "Énergie", "Toulouse", "France", 410, "https://energieverte.example", "Supervision industrielle et cloud."),
    ("ÉduForm", "Éducation", "Nantes", "France", 48, "https://eduform.example", "Campus, Microsoft 365 et filtrage."),
    ("ImmoHorizon", "Immobilier", "Bordeaux", "France", 32, "https://immohorizon.example", "Agence, CRM et sauvegarde."),
    ("CyberNord", "Informatique", "Lille", "France", 22, "https://cybernord.example", "ESN locale, partenariat infogérance."),
    ("Atelier Mécanique du Rhône", "Industrie", "Lyon", "France", 75, "https://amr.example", "Parc machines, besoin MES léger."),
    ("Assuréa", "Assurance", "Paris", "France", 190, "https://assurea.example", "Mutuelle, conformité et SOC."),
    ("BioLab Ouest", "Santé", "Nantes", "France", 110, "https://biolab.example", "Laboratoire, LIMS et réseau."),
    ("LogiSeine", "Transport", "Paris", "France", 260, "https://logiseine.example", "Entrepôt, WMS et Wi-Fi industriel."),
    ("Maison des Saveurs", "Commerce", "Bordeaux", "France", 18, "https://mds.example", "Épicerie fine, caisse et site."),
    ("HelioTech", "Technologie", "Toulouse", "France", 95, "https://heliotech.example", "Startup hardware, infra et ISO 27001."),
    ("Cabinet Dumont", "Finance", "Lyon", "France", 14, "https://dumont.example", "Expertise comptable, sauvegarde et 365."),
    ("Port Atlantique Services", "Transport", "Nantes", "France", 150, "https://pas.example", "Manutention portuaire, radio et SI."),
    ("GreenWatt Belgique", "Énergie", "Bruxelles", "Belgique", 80, "https://greenwatt-be.example", "Filiale belge, infogérance francophone."),
    ("Clinique des Alpes", "Santé", "Genève", "Suisse", 130, "https://cda.example", "Établissement privé, DPI et réseau."),
    ("TechBridge", "Informatique", "Paris", "France", 45, "https://techbridge.example", "Intégrateur, besoin sous-traitance cloud."),
]

STATUSES = ["NEW", "QUALIFIED", "CONTACTED", "FOLLOW_UP", "NEGOTIATION", "CONVERTED", "LOST", "LATER"]
PRIORITIES = ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
VALUES = [8000, 12000, 18000, 25000, 32000, 45000, 60000, 90000]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count():
            print("Base déjà peuplée.")
            return

        admin = User(name="Léa Martin", email="admin@example.com", password_hash=get_password_hash("Admin123!"), role="ADMIN")
        commercial = User(name="Thomas Bernard", email="commercial@example.com", password_hash=get_password_hash("Commercial123!"), role="COMMERCIAL")
        manager = User(name="Sophie Dubois", email="manager@example.com", password_hash=get_password_hash("Manager123!"), role="MANAGER")
        db.add_all([admin, commercial, manager])
        db.commit()

        companies = []
        for name, industry, city, country, employees, website, description in COMPANIES:
            company = Company(
                name=name,
                industry=industry,
                city=city,
                country=country,
                employee_count=employees,
                website=website,
                email=f"contact@{name.lower().replace(' ', '').replace('é', 'e')[:12]}.fr",
                phone="01 84 00 00 00",
                address="12 rue de l'Innovation",
                description=description,
                source="Base interne",
            )
            db.add(company)
            companies.append(company)
        db.commit()

        now = datetime.now(timezone.utc)
        prospects = []
        for index, company in enumerate(companies):
            assignee = commercial if index % 3 else manager
            prospect = Prospect(
                company_id=company.id,
                assigned_to=assignee.id,
                status=STATUSES[index % len(STATUSES)],
                priority=PRIORITIES[index % len(PRIORITIES)],
                estimated_value=VALUES[index % len(VALUES)],
                notes="Besoin cloud, cybersécurité et infogérance à qualifier.",
            )
            db.add(prospect)
            prospects.append(prospect)
        extra = Prospect(
            company_id=companies[0].id,
            assigned_to=commercial.id,
            status="FOLLOW_UP",
            priority="VERY_HIGH",
            estimated_value=72000,
            notes="Budget ERP validé, relance commerciale urgente.",
        )
        db.add(extra)
        prospects.append(extra)
        db.commit()

        for prospect in prospects:
            db.add(
                Contact(
                    prospect_id=prospect.id,
                    first_name="Camille",
                    last_name="Roux",
                    job_title="DSI",
                    email="dsi@example.com",
                    phone="06 12 34 56 78",
                    linkedin_url="https://linkedin.com/in/camille-roux",
                )
            )
            db.add(
                Contact(
                    prospect_id=prospect.id,
                    first_name="Nicolas",
                    last_name="Petit",
                    job_title="Directeur général",
                    email="dg@example.com",
                    phone="06 98 76 54 32",
                )
            )
            db.add(
                Activity(
                    prospect_id=prospect.id,
                    user_id=commercial.id,
                    type="PHONE",
                    subject="Appel de découverte",
                    description="Le prospect souhaite recevoir une proposition.",
                    completed_at=now - timedelta(days=8),
                    result="Intérêt confirmé",
                )
            )
            db.add(
                Activity(
                    prospect_id=prospect.id,
                    user_id=commercial.id,
                    type="EMAIL",
                    subject="Proposition commerciale envoyée",
                    description="Proposition commerciale envoyée.",
                    completed_at=now - timedelta(days=5),
                )
            )
            due = now + timedelta(days=(prospect.id % 5) - 1)
            db.add(
                FollowUp(
                    prospect_id=prospect.id,
                    assigned_to=commercial.id,
                    due_date=due,
                    reminder_date=due - timedelta(hours=4),
                    status="PENDING",
                    notes="Relancer le prospect.",
                )
            )
            if prospect.status == "CONVERTED":
                db.add(
                    Conversion(
                        prospect_id=prospect.id,
                        converted_by=commercial.id,
                        department="Technique",
                        value=prospect.estimated_value,
                        notes="Converti et transmis au pôle technique.",
                    )
                )
        db.commit()

        for prospect in db.query(Prospect).all():
            qualification = qualify_prospect(db, prospect)
            prospect.score = qualification.score
            prospect.priority = qualification.priority.value
            db.add(
                AIEvaluation(
                    prospect_id=prospect.id,
                    score=qualification.score,
                    reasoning=" | ".join(f"{c.label} (+{c.points})" for c in qualification.criteria),
                    recommendation=qualification.summary,
                )
            )
        db.commit()
        print("Données de démonstration créées.")
        print("Comptes : admin@example.com / Admin123!")
        print("          commercial@example.com / Commercial123!")
        print("          manager@example.com / Manager123!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
