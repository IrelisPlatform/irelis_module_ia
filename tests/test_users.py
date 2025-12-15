from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """Verify the health endpoint responds 200 and with status text."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
