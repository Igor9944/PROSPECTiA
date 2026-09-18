from fastapi.testclient import TestClient

from tests.conftest import auth_headers


def test_login_success(client: TestClient, users):
    response = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "Admin123!"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure(client: TestClient, users):
    response = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "wrong"})
    assert response.status_code == 401


def test_me(client: TestClient, users):
    headers = auth_headers(client, "admin@example.com", "Admin123!")
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"
    assert "password_hash" not in response.json()
