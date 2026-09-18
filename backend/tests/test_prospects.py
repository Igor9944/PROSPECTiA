from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Company
from tests.conftest import auth_headers


def _company(db: Session) -> Company:
    company = Company(name="TestCorp", industry="Informatique", city="Paris", country="France", employee_count=80)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def test_prospect_crud_status_activity_followup_conversion_ai(client: TestClient, db: Session, users):
    headers = auth_headers(client, "commercial@example.com", "Commercial123!")
    company = _company(db)

    created = client.post(
        "/api/prospects/",
        json={"company_id": company.id, "assigned_to": users["commercial"].id, "notes": "Besoin cloud"},
        headers=headers,
    )
    assert created.status_code == 201
    prospect_id = created.json()["id"]
    assert created.json()["score"] >= 0

    fetched = client.get(f"/api/prospects/{prospect_id}", headers=headers)
    assert fetched.status_code == 200

    updated = client.patch(f"/api/prospects/{prospect_id}", json={"notes": "Budget confirmé"}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["notes"] == "Budget confirmé"

    status_res = client.patch(f"/api/prospects/{prospect_id}/status", json={"status": "CONTACTED"}, headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "CONTACTED"

    activity = client.post(
        "/api/activities/",
        json={"prospect_id": prospect_id, "type": "PHONE", "subject": "Appel"},
        headers=headers,
    )
    assert activity.status_code == 201

    follow_up = client.post(
        "/api/follow-ups/",
        json={
            "prospect_id": prospect_id,
            "assigned_to": users["commercial"].id,
            "due_date": "2026-09-20T09:00:00Z",
            "notes": "Relancer",
        },
        headers=headers,
    )
    assert follow_up.status_code == 201

    conversion = client.post(
        "/api/conversions/",
        json={"prospect_id": prospect_id, "department": "Technique", "value": 15000},
        headers=headers,
    )
    assert conversion.status_code == 201

    ai = client.post(f"/api/ai/prospects/{prospect_id}/analyze", headers=headers)
    assert ai.status_code == 200
    assert 0 <= ai.json()["score"] <= 100
    assert ai.json()["reasoning"]

    deleted = client.delete(f"/api/prospects/{prospect_id}", headers=headers)
    assert deleted.status_code == 200


def test_permissions_users_forbidden_for_commercial(client: TestClient, users):
    headers = auth_headers(client, "commercial@example.com", "Commercial123!")
    response = client.get("/api/users/", headers=headers)
    assert response.status_code == 403


def test_permissions_users_ok_for_admin(client: TestClient, users):
    headers = auth_headers(client, "admin@example.com", "Admin123!")
    response = client.get("/api/users/", headers=headers)
    assert response.status_code == 200
