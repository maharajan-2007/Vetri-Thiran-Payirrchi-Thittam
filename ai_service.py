import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = None
if genai and GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
    client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_INSTRUCTION = """
You are FitBuddy, a professional fitness-planning assistant.
Create practical, structured and motivating fitness guidance.
Do not diagnose medical conditions or claim to replace a doctor or qualified trainer.
If a user has pain, injury, medical conditions, pregnancy, or other health concerns,
recommend professional medical/fitness guidance before strenuous exercise.
Keep recommendations appropriate to the user's stated age, goal and intensity.
"""


def is_gemini_configured() -> bool:
    return client is not None


def _generate(prompt: str) -> str:
    if not client:
        return (
            "Gemini API key is not configured. "
            "Create a .env file and set GEMINI_API_KEY."
        )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            ),
        )
        text = getattr(response, "text", None)
        if text:
            return text.strip()
        return "Gemini returned an empty response."
    except Exception as exc:
        return f"Failed to generate AI response: {exc}"


def generate_workout_plan(
    name: str,
    age: int,
    gender: str,
    weight: int,
    goal: str,
    intensity: str,
) -> str:
    prompt = f"""
Create a personalized 7-day workout plan for the following user.

User Profile
- Name: {name}
- Age: {age}
- Gender: {gender}
- Weight: {weight} kg
- Primary Goal: {goal}
- Preferred Workout Intensity: {intensity}

Requirements:
1. Produce a clear Day 1 through Day 7 schedule.
2. Include warm-up and cool-down guidance.
3. For workout days, include exercise names, sets, reps or duration, and rest.
4. Include rest/recovery days where appropriate.
5. Match the requested goal and intensity.
6. Do not prescribe unsafe or extreme training.
7. End with concise recovery and hydration guidance.
8. Use plain Markdown with headings and bullet lists.
"""
    return _generate(prompt)


def revise_workout_plan(current_plan: str, feedback: str) -> str:
    prompt = f"""
Revise the existing FitBuddy 7-day workout plan using the user's feedback.

EXISTING PLAN
---
{current_plan}
---

USER FEEDBACK
---
{feedback}
---

Requirements:
- Preserve useful parts that the user did not ask to change.
- Apply the feedback specifically and clearly.
- Keep the result as a complete 7-day plan.
- Keep exercise volume realistic for the stated context.
- Use plain Markdown.
"""
    return _generate(prompt)


def generate_nutrition_tip(goal: str) -> str:
    prompt = f"""
Give one concise, practical nutrition or recovery tip for this fitness goal:
{goal}

Return only 1-2 sentences. Avoid diagnosing conditions or giving medical treatment.
"""
    return _generate(prompt)
