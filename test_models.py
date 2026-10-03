from database import Base
from models import User, WorkoutPlan, Feedback


def test_models_are_registered():
    tables = set(Base.metadata.tables.keys())
    assert "users" in tables
    assert "workout_plans" in tables
    assert "feedbacks" in tables


def test_relationships_exist():
    assert hasattr(User, "plans")
    assert hasattr(WorkoutPlan, "user")
    assert hasattr(WorkoutPlan, "feedbacks")
    assert hasattr(Feedback, "plan")
