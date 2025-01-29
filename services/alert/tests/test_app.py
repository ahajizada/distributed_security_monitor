import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_alert():
    test_alert = {
        "severity": "HIGH",
        "message": "Security breach detected",
        "metadata": {"source": "IDS"},
        "timestamp": datetime.utcnow().isoformat()
    }
    response = client.post("/alerts", json=test_alert)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_create_alert_invalid_data():
    test_alert = {
        "severity": "HIGH"
    }
    response = client.post("/alerts", json=test_alert)
    assert response.status_code == 422
