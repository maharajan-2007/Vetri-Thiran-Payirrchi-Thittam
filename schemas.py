from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class FeedbackBase(BaseModel):
    feedback_text: str


class FeedbackCreate(FeedbackBase):
    plan_id: int


class Feedback(FeedbackBase):
    id: int
    plan_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkoutPlanBase(BaseModel):
    plan_content: str


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


class WorkoutPlan(WorkoutPlanBase):
    id: int
    user_id: int
    created_at: datetime
    feedbacks: List[Feedback] = []

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    name: str
    age: int
    gender: str
    weight: int
    goal: str
    intensity: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    plans: List[WorkoutPlan] = []

    model_config = ConfigDict(from_attributes=True)
