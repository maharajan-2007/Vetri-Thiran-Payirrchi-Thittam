from .gemini_service import generate_text
from .schemas import Goal


def _fallback_tip(goal: Goal) -> str:
    tips = {
        "weight loss": "Build meals around vegetables, a protein source, high-fiber carbohydrates, and water. Sustainable calorie control is more useful than extreme restriction.",
        "muscle gain": "Include a protein-rich food at each meal, hydrate well, and pair resistance training with adequate sleep and recovery.",
        "general wellness": "Aim for regular balanced meals, plenty of vegetables and fruit, adequate protein, hydration, and consistent sleep.",
        "flexibility": "Stay hydrated and include a variety of whole foods; recovery and regular mobility practice work together.",
        "endurance": "Prioritize carbohydrates from whole-food sources around longer sessions, adequate protein, fluids, and recovery.",
    }
    return tips[goal]


def generate_nutrition_tip_with_flash(goal: Goal) -> str:
    prompt = f"""
Give one concise, practical nutrition or recovery tip for someone whose fitness goal is "{goal}".
Use 2–4 sentences. Avoid medical claims, supplements as treatment, extreme calorie restriction,
and individualized medical nutrition advice.
"""
    return generate_text(
        prompt,
        model_kind="fast",
        fallback=lambda: _fallback_tip(goal),
    )
