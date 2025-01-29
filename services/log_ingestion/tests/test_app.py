import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_ingest_log_success():
    test_log = {
        "source": "test-source",
        "timestamp": datetime.utcnow().isoformat(),
        "level": "INFO",
        "message": "Test message",
        "metadata": {"test": "data"}
    }
    response = client.post("/logs", json=test_log)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_ingest_log_invalid_data():
    test_log = {
        "source": "test-source",
    }
    response = client.post("/logs", json=test_log)
    assert response.status_code == 422
