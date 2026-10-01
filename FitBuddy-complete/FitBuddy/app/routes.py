from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .database_service import (
    delete_user,
    get_all_plans,
    get_all_users,
    get_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def _render_result(request: Request, user, plan, message: str | None = None):
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "plan": plan,
            "message": message,
        },
    )


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user_input = UserInput(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=422,
        )

    user = save_user(db, user_input)
    workout = generate_workout_gemini(user_input)
    tip = generate_nutrition_tip_with_flash(user_input.goal)
    plan = save_plan(db, user_input.user_id, workout, tip)

    return _render_result(request, user, plan)


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        payload = FeedbackRequest(user_id=user_id, feedback=feedback)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    user = get_user(db, payload.user_id)
    plan = get_plan(db, payload.user_id)
    if not user or not plan:
        raise HTTPException(status_code=404, detail="User or workout plan not found.")

    revised = update_workout_plan(plan.original_plan, payload.feedback)
    update_plan(db, plan, revised, payload.feedback)

    return _render_result(
        request,
        user,
        plan,
        "Your feedback has been applied to the latest plan.",
    )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, token: str | None = None, db: Session = Depends(get_db)):
    if token != settings.admin_token:
        raise HTTPException(
            status_code=403,
            detail="Admin token required. Open /view-all-users?token=YOUR_ADMIN_TOKEN",
        )
    users = get_all_users(db)
    plans = {p.user_id: p for p in get_all_plans(db)}
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users, "plans": plans, "token": token},
    )


@router.post("/admin/delete/{user_id}")
def admin_delete_user(user_id: str, token: str = Form(...), db: Session = Depends(get_db)):
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Invalid admin token.")
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found.")
    return {"ok": True, "message": f"Deleted user {user_id}."}


# JSON API endpoints for integrations/mobile clients/testing.
api_router = APIRouter(prefix="/api")


@api_router.post("/generate-workout")
def api_generate_workout(payload: UserInput, db: Session = Depends(get_db)):
    user = save_user(db, payload)
    workout = generate_workout_gemini(payload)
    tip = generate_nutrition_tip_with_flash(payload.goal)
    plan = save_plan(db, payload.user_id, workout, tip)
    return {
        "user": user,
        "plan_id": plan.id,
        "workout_plan": plan.original_plan,
        "nutrition_tip": plan.nutrition_tip,
    }


@api_router.post("/submit-feedback")
def api_submit_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    user = get_user(db, payload.user_id)
    plan = get_plan(db, payload.user_id)
    if not user or not plan:
        raise HTTPException(status_code=404, detail="User or workout plan not found.")
    revised = update_workout_plan(plan.original_plan, payload.feedback)
    update_plan(db, plan, revised, payload.feedback)
    return {
        "user_id": payload.user_id,
        "plan_id": plan.id,
        "updated_plan": plan.updated_plan,
        "feedback": plan.feedback,
    }


@api_router.get("/users/{user_id}")
def api_get_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    plan = get_plan(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return {
        "user": user,
        "plan": plan,
    }


@api_router.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
