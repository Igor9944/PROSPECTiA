from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.company import Company
from app.models.contact import Contact
from app.models.enums import ProspectPriority
from app.models.prospect import Prospect
from app.schemas.prospect import QualificationCriterion, QualificationOut

HIGH_VALUE_INDUSTRIES = {
    "Informatique",
    "Technologie",
    "Finance",
    "Assurance",
    "Santé",
    "Énergie",
}
MEDIUM_VALUE_INDUSTRIES = {"Industrie", "Transport", "Éducation", "Immobilier", "Commerce"}
TARGET_CITIES = {"Paris", "Lyon", "Lille", "Nantes", "Toulouse", "Bordeaux", "Marseille"}


def score_level(score: int) -> str:
    if score <= 30:
        return "faible"
    if score <= 60:
        return "moyen"
    if score <= 80:
        return "élevé"
    return "très élevé"


def priority_from_score(score: int) -> ProspectPriority:
    if score <= 30:
        return ProspectPriority.LOW
    if score <= 60:
        return ProspectPriority.MEDIUM
    if score <= 80:
        return ProspectPriority.HIGH
    return ProspectPriority.VERY_HIGH


def qualify_prospect(db: Session, prospect: Prospect) -> QualificationOut:
    company: Company | None = prospect.company or db.get(Company, prospect.company_id)
    contacts = db.query(Contact).filter(Contact.prospect_id == prospect.id).all()
    activities = db.query(Activity).filter(Activity.prospect_id == prospect.id).all()
    criteria: list[QualificationCriterion] = []
    score = 0

    employees = company.employee_count if company else 0
    if employees and employees >= 250:
        points = 22
        explanation = f"{employees} collaborateurs : compte stratégique."
    elif employees and employees >= 50:
        points = 18
        explanation = f"{employees} collaborateurs : PME structurée, bon potentiel."
    elif employees and employees >= 10:
        points = 12
        explanation = f"{employees} collaborateurs : TPE/PME accessible."
    else:
        points = 6
        explanation = "Taille peu renseignée ou très petite structure."
    score += points
    criteria.append(QualificationCriterion(label="Taille de l'entreprise", points=points, explanation=explanation))

    industry = company.industry if company else None
    if industry in HIGH_VALUE_INDUSTRIES:
        points = 20
        explanation = f"Secteur {industry} fortement aligné avec les solutions IT."
    elif industry in MEDIUM_VALUE_INDUSTRIES:
        points = 12
        explanation = f"Secteur {industry} pertinent, besoins IT habituels."
    else:
        points = 6
        explanation = f"Secteur {industry or 'inconnu'} moins prioritaire."
    score += points
    criteria.append(QualificationCriterion(label="Secteur d'activité", points=points, explanation=explanation))

    city = company.city if company else None
    country = company.country if company else None
    if city in TARGET_CITIES:
        points = 12
        explanation = f"{city} : zone commerciale prioritaire."
    elif country in {"France", "Belgique", "Suisse"}:
        points = 8
        explanation = f"{country} : marché francophone adressable."
    else:
        points = 4
        explanation = "Localisation moins prioritaire ou inconnue."
    score += points
    criteria.append(QualificationCriterion(label="Localisation", points=points, explanation=explanation))

    info_bits = 0
    if company:
        info_bits += sum(1 for value in [company.website, company.email, company.phone, company.description] if value)
    if info_bits >= 3:
        points = 12
        explanation = "Fiche entreprise complète, qualification fiable."
    elif info_bits >= 1:
        points = 7
        explanation = "Informations partielles, à enrichir avant closing."
    else:
        points = 3
        explanation = "Peu d'informations disponibles."
    score += points
    criteria.append(QualificationCriterion(label="Informations disponibles", points=points, explanation=explanation))

    if len(contacts) >= 2:
        points = 12
        explanation = f"{len(contacts)} interlocuteurs identifiés."
    elif len(contacts) == 1:
        points = 8
        explanation = "Un contact nominatif est déjà connu."
    else:
        points = 3
        explanation = "Aucun contact identifié."
    score += points
    criteria.append(QualificationCriterion(label="Contacts", points=points, explanation=explanation))

    now = datetime.now(timezone.utc)
    recent = []
    for activity in activities:
        created = activity.created_at
        if not created:
            continue
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        if (now - created).days <= 45:
            recent.append(activity)
    if len(recent) >= 3:
        points = 14
        explanation = "Plusieurs interactions récentes : engagement réel."
    elif recent:
        points = 9
        explanation = "Au moins une interaction récente."
    elif activities:
        points = 5
        explanation = "Historique ancien, relance nécessaire."
    else:
        points = 2
        explanation = "Aucune interaction enregistrée."
    score += points
    criteria.append(QualificationCriterion(label="Interactions", points=points, explanation=explanation))

    notes = (prospect.notes or "").lower()
    if any(keyword in notes for keyword in ["erp", "cloud", "cybersécurité", "infra", "besoin", "budget"]):
        points = 8
        explanation = "Les notes mentionnent un besoin IT explicite."
    else:
        points = 3
        explanation = "Besoin potentiel à confirmer en découverte."
    score += points
    criteria.append(QualificationCriterion(label="Besoins potentiels", points=points, explanation=explanation))

    score = max(0, min(100, score))
    level = score_level(score)
    summary = (
        f"Score {score}/100 ({level}). "
        f"Les critères les plus favorables : {', '.join(c.label for c in sorted(criteria, key=lambda x: x.points, reverse=True)[:3])}."
    )
    return QualificationOut(
        score=score,
        level=level,
        priority=priority_from_score(score),
        criteria=criteria,
        summary=summary,
    )
