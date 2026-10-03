from fastapi import FastAPI, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import crud
import database
import models
import schemas
import ai_service

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="Personalized 7-day fitness plans powered by Google Gemini.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc()).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "users": users,
        },
    )


@app.post("/users", response_model=schemas.User)
def create_or_update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user.name)
    if db_user:
        return crud.update_user(db, db_user, user)
    return crud.create_user(db, user)


@app.post("/generate_plan")
def generate_workout_plan(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    if age < 13 or age > 100:
        raise HTTPException(status_code=400, detail="Age must be between 13 and 100.")
    if weight < 20 or weight > 500:
        raise HTTPException(status_code=400, detail="Please enter a valid weight.")

    user_data = schemas.UserCreate(
        name=name.strip(),
        age=age,
        gender=gender,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    db_user = crud.get_user_by_name(db, name=user_data.name)
    if not db_user:
        db_user = crud.create_user(db, user_data)
    else:
        db_user = crud.update_user(db, db_user, user_data)

    plan_text = ai_service.generate_workout_plan(
        name=db_user.name,
        age=db_user.age,
        gender=db_user.gender,
        weight=db_user.weight,
        goal=db_user.goal,
        intensity=db_user.intensity,
    )

    db_plan = crud.create_workout_plan(
        db,
        plan_content=plan_text,
        user_id=db_user.id,
    )

    return {
        "status": "success",
        "user_id": db_user.id,
        "plan_id": db_plan.id,
        "plan": plan_text,
    }


@app.get("/users/{user_id}/latest_plan")
def get_latest_plan(user_id: int, db: Session = Depends(get_db)):
    db_plan = crud.get_latest_workout_plan(db, user_id=user_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {"plan_id": db_plan.id, "plan_content": db_plan.plan_content}


@app.post("/update_plan")
def update_workout_plan(
    plan_id: int = Form(...),
    feedback_text: str = Form(...),
    db: Session = Depends(get_db),
):
    db_plan = crud.get_workout_plan(db, plan_id=plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found.")

    feedback_text = feedback_text.strip()
    if not feedback_text:
        raise HTTPException(status_code=400, detail="Feedback cannot be empty.")

    crud.create_feedback(
        db,
        schemas.FeedbackCreate(
            plan_id=plan_id,
            feedback_text=feedback_text,
        ),
    )

    new_plan_text = ai_service.revise_workout_plan(
        current_plan=db_plan.plan_content,
        feedback=feedback_text,
    )

    db_plan = crud.update_workout_plan(
        db,
        db_plan,
        new_plan_text,
    )

    return {
        "status": "success",
        "plan_id": db_plan.id,
        "plan": db_plan.plan_content,
    }


@app.get("/nutrition_tip")
def get_nutrition_tip(goal: str):
    goal = goal.strip()
    if not goal:
        raise HTTPException(status_code=400, detail="Goal is required.")
    return {"goal": goal, "tip": ai_service.generate_nutrition_tip(goal)}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "gemini_configured": ai_service.is_gemini_configured(),
    }
