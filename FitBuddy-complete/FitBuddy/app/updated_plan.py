from .gemini_service import generate_text


def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""
Revise the existing FitBuddy 7-day workout plan using the user's feedback.

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Requirements:
- Preserve the 7-day structure unless the feedback asks for a change.
- Make the requested changes explicit.
- Keep the plan practical and safe.
- Include warm-up, main workout, cooldown/recovery where appropriate.
- Do not prescribe treatment or claim to diagnose health conditions.
- Return only the revised plan plus a brief safety note.
"""
    return generate_text(
        prompt,
        model_kind="workout",
        fallback=lambda: (
            original_plan
            + "\n\n--- FEEDBACK APPLIED LOCALLY ---\n"
            + feedback.strip()
            + "\n\nThe AI service was unavailable, so the original plan was preserved. "
              "Please retry after configuring Gemini if you want an AI-generated revision."
        ),
    )
