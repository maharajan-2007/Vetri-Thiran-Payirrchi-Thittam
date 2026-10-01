from collections.abc import Callable

from .config import settings

try:
    from google import genai
    from google.genai import types
except ImportError:  # Allows local fallback mode to work before dependencies are installed.
    genai = None
    types = None


_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    if not settings.gemini_api_key or genai is None:
        return None
    _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


def generate_text(prompt: str, model_kind: str, fallback: Callable[[], str]) -> str:
    client = _get_client()
    if client is None:
        return fallback()

    model = settings.workout_model if model_kind == "workout" else settings.fast_model
    try:
        config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=5000 if model_kind == "workout" else 500,
        )
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        text = (response.text or "").strip()
        return text if text else fallback()
    except Exception:
        # The UI remains usable if the remote model is unavailable or rate-limited.
        return fallback()
