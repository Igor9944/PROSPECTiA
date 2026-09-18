import pytest

from app.models import Company, Prospect
from app.services.ai_service import get_ai_provider
from app.services.qualification import qualify_prospect


def test_ai_score_is_explained(db, users):
    company = Company(
        name="ScoreCorp",
        industry="Informatique",
        city="Paris",
        country="France",
        employee_count=300,
        website="https://score.example",
        email="it@score.example",
        phone="0102030405",
        description="Cloud et cybersécurité",
    )
    db.add(company)
    db.commit()
    prospect = Prospect(company_id=company.id, assigned_to=users["commercial"].id, notes="Besoin cloud")
    db.add(prospect)
    db.commit()
    result = qualify_prospect(db, prospect)
    assert 0 <= result.score <= 100
    assert result.criteria
    assert all(item.explanation for item in result.criteria)


def test_google_ai_provider_is_selected(monkeypatch):
    monkeypatch.setattr("app.services.ai_service.settings.AI_PROVIDER", "google")
    provider = get_ai_provider()
    assert provider.name == "google"
