from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_workout_without_api_key():
    response = client.post(
        "/api/generate-workout",
        json={
            "user_id": "test-user",
            "name": "Test User",
            "age": 25,
            "weight": 70,
            "goal": "general wellness",
            "intensity": "medium",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["plan_id"]
    assert "Day 1" in body["workout_plan"]
    assert body["nutrition_tip"]


def test_feedback_without_api_key():
    response = client.post(
        "/api/submit-feedback",
        json={
            "user_id": "test-user",
            "feedback": "Add more recovery work.",
        },
    )
    assert response.status_code == 200
    assert response.json()["updated_plan"]
