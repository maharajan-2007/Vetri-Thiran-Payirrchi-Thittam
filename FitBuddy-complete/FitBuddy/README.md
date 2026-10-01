# FitBuddy – AI Fitness Plan Generator

A complete FastAPI + Jinja2 + SQLite application based on the supplied FitBuddy project specification.

## Features

- Personalized 7-day workout generation
- Nutrition/recovery tip generation
- Feedback-based plan revision
- SQLite persistence with SQLAlchemy
- Jinja2 web UI
- Admin dashboard with user/plan visibility and deletion
- JSON API endpoints
- Automatic local fallback when `GEMINI_API_KEY` is missing, so the app can be tested before connecting Gemini
- Pytest tests

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── database_service.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── gemini_service.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static/
│   └── style.css
├── templates/
│   ├── all_users.html
│   ├── base.html
│   ├── index.html
│   └── result.html
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code setup – Windows

1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create the virtual environment:

```powershell
python -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Create `.env` from `.env.example`.
8. Add your Gemini API key to `.env`.
9. Start the server:

```powershell
uvicorn app.main:app --reload
```

10. Open:

- Web app: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health

## Gemini API key

Create a Gemini API key in Google AI Studio, then put it in `.env`:

```env
GEMINI_API_KEY=your_real_key
```

The application uses `google-genai`, Google's current Python SDK. The default model variables are configurable in `.env`.

If no API key is configured, FitBuddy uses a deterministic local fallback for development/testing. This fallback is not Gemini output.

## Admin dashboard

Set a strong value in `.env`:

```env
ADMIN_TOKEN=your-secret-admin-token
```

Then visit:

```text
http://127.0.0.1:8000/view-all-users?token=your-secret-admin-token
```

Do not expose this token publicly. For production, replace this simple token mechanism with proper authentication and authorization.

## Test

Run:

```powershell
pytest -q
```

The tests work without a Gemini API key because the project has a local fallback mode.

## API examples

### Generate

`POST /api/generate-workout`

```json
{
  "user_id": "user001",
  "name": "Alex",
  "age": 25,
  "weight": 70,
  "goal": "muscle gain",
  "intensity": "medium"
}
```

### Update with feedback

`POST /api/submit-feedback`

```json
{
  "user_id": "user001",
  "feedback": "Add more cardio and make Day 6 a recovery day."
}
```

### Get user

`GET /api/users/user001`

## Notes

This project follows the supplied documentation's core architecture but modernizes the Gemini integration and adds validation, a service layer, API schemas, test coverage, safer configuration handling, and graceful AI-service failure behavior.

Fitness plans are general wellness guidance. Users with injuries, medical conditions, pregnancy, or other individual concerns should consult an appropriately qualified professional before following an exercise or nutrition program.
