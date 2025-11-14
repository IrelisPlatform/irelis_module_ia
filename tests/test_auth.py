from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_requires_credentials() -> None:
    response = client.post("/api/v1/auth/login", data={"username": "", "password": ""})
    assert response.status_code in (400, 401)
