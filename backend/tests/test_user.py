from fastapi.testclient import TestClient

from tests.conftest import auth_headers


def test_register_and_login_with_auth_api(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test.user@example.com",
            "password": "StrongPass123!",
            "role": "COMMERCIAL",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "test.user@example.com"
    assert body["name"] == "Test User"
    assert "password_hash" not in body

    login = client.post(
        "/api/auth/login",
        json={"email": "test.user@example.com", "password": "StrongPass123!"},
    )
    assert login.status_code == 200
    assert "access_token" in login.json()

    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    me = client.get("/api/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "test.user@example.com"


def test_duplicate_email_is_rejected(client: TestClient, users):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Duplicate User",
            "email": "admin@example.com",
            "password": "StrongPass123!",
            "role": "ADMIN",
        },
    )
    assert response.status_code == 400
    assert "déjà" in response.json()["detail"].lower() or "used" in response.json()["detail"].lower()


def test_admin_can_list_users(client: TestClient, users):
    headers = auth_headers(client, "admin@example.com", "Admin123!")
    response = client.get("/api/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 2
