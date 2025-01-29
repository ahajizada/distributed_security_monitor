import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_log():
    test_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "ERROR",
        "message": "Suspicious activity detected",
        "metadata": {"source_reliability": 0.8}
    }
    response = client.post("/analyze", json=test_log)
    assert response.status_code == 200
    assert "threat_score" in response.json()
    assert "is_threat" in response.json()

def test_analyze_log_invalid_data():
    test_log = {
        # Missing required fields
    }
    response = client.post("/analyze", json=test_log)
    assert response.status_code == 500
