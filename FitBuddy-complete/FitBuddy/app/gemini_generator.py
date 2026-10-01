from .gemini_service import generate_text
from .schemas import UserInput


def _fallback_plan(user: UserInput) -> str:
    intensity = user.intensity.capitalize()
    goal = user.goal.capitalize()
    return f"""FITBUDDY 7-DAY WORKOUT PLAN
Goal: {goal}
Intensity: {intensity}
Profile: {user.age} years, {user.weight:.1f} kg

Day 1 – Full Body
Warm-up: 5–10 min brisk walk + mobility.
Main: Squats 3x10, push-ups 3x8–12, dumbbell rows 3x10, glute bridges 3x12.
Cooldown: 5 min easy walking and stretching.

Day 2 – Cardio + Core
Warm-up: 5 min easy movement.
Main: 20–30 min brisk walking/cycling; plank 3x20–40 sec; dead bug 3x10/side.
Cooldown: Gentle stretching.

Day 3 – Recovery
20–30 min easy walking plus mobility. Keep effort light.

Day 4 – Upper Body
Warm-up: 5–10 min.
Main: Incline push-ups 3x10, rows 3x10, shoulder press 3x10, curls 2x12.
Cooldown: Shoulder and upper-back stretches.

Day 5 – Lower Body
Warm-up: 5–10 min.
Main: Squats 3x10, reverse lunges 3x8/side, hip hinge 3x10, calf raises 3x15.
Cooldown: Easy walking and leg stretches.

Day 6 – Cardio + Mobility
30–40 min moderate cardio, followed by 10 min mobility.

Day 7 – Rest / Active Recovery
Easy walk and gentle stretching. Prioritize sleep and hydration.

Progression: Increase volume gradually only when the current workload feels manageable.
Safety: Stop if you feel sharp pain, dizziness, chest pain, or unusual shortness of breath.
"""


def generate_workout_gemini(user: UserInput) -> str:
    prompt = f"""
Create a practical, beginner-friendly 7-day fitness plan for this user.

Name: {user.name}
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Preferred intensity: {user.intensity}

Requirements:
- Exactly 7 labeled days.
- Include warm-up, main workout, and cooldown/recovery.
- Give exercise sets/reps or durations and sensible rest intervals.
- Include at least one recovery/rest-focused day.
- Tailor the plan to the goal and requested intensity.
- Do not diagnose conditions, prescribe medication, or give extreme dieting advice.
- Keep the plan clear enough to follow without additional formatting.
- Add a short safety note at the end.
"""
    return generate_text(prompt, model_kind="workout", fallback=lambda: _fallback_plan(user))
