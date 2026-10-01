from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Plan, User
from .schemas import UserInput


def save_user(db: Session, user: UserInput) -> User:
    existing = db.scalar(select(User).where(User.user_id == user.user_id))
    if existing:
        existing.name = user.name
        existing.age = user.age
        existing.weight = user.weight
        existing.goal = user.goal
        existing.intensity = user.intensity
        db.commit()
        db.refresh(existing)
        return existing

    record = User(**user.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def save_plan(db: Session, user_id: str, original_plan: str, nutrition_tip: str) -> Plan:
    plan = Plan(
        user_id=user_id,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_user(db: Session, user_id: str) -> User | None:
    return db.scalar(select(User).where(User.user_id == user_id))


def get_plan(db: Session, user_id: str) -> Plan | None:
    return db.scalar(
        select(Plan).where(Plan.user_id == user_id).order_by(Plan.id.desc())
    )


def update_plan(db: Session, plan: Plan, revised_plan: str, feedback: str) -> Plan:
    plan.updated_plan = revised_plan
    plan.feedback = feedback
    db.commit()
    db.refresh(plan)
    return plan


def get_all_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


def get_all_plans(db: Session) -> list[Plan]:
    return list(db.scalars(select(Plan).order_by(Plan.created_at.desc())).all())


def delete_user(db: Session, user_id: str) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.query(Plan).filter(Plan.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return True
