# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is a FastAPI + SQLite + HTML/CSS/JavaScript fitness application that uses Google Gemini to generate personalized 7-day workout plans, revise them from user feedback, and provide nutrition/recovery tips.

## Project structure

```text
FitBuddy/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── ai_service.py
├── requirements.txt
├── .env.example
├── .gitignore
├── test_models.py
├── fitbuddy.db                 # created automatically
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 1. Open the project

Open the `FitBuddy` folder in VS Code.

## 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Create `.env`

Copy `.env.example` to `.env`.

Put your Gemini API key in:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never upload `.env` or your API key to GitHub.

## 5. Check dependencies

```bash
python -c "import fastapi, sqlalchemy, google.genai; print('FitBuddy dependencies OK')"
```

Expected:

```text
FitBuddy dependencies OK
```

## 6. Test the models

```bash
pytest -q
```

## 7. Start FastAPI

```bash
uvicorn main:app --reload
```

## 8. Open FitBuddy

Open:

```text
http://127.0.0.1:8000
```

or:

```text
http://localhost:8000
```

## 9. Test AI workout generation

Enter:
- Name
- Age
- Gender
- Weight
- Goal
- Intensity

Then click **Generate 7-Day Plan**.

## 10. Test feedback refinement

After a plan is generated, enter feedback such as:

```text
Add more cardio and make Day 3 a lighter recovery day.
```

Click **Revise Plan**.

## 11. Test nutrition tip

Click **Get Tip** in the Nutrition & Recovery section.

## API endpoints

- `GET /` – FitBuddy web UI
- `GET /health` – health/configuration check
- `POST /users` – create/update user
- `POST /generate_plan` – generate and save a 7-day plan
- `GET /users/{user_id}/latest_plan` – get the latest plan
- `POST /update_plan` – revise a plan from feedback
- `GET /nutrition_tip?goal=...` – generate a nutrition/recovery tip

## Important note

FitBuddy is general fitness software. AI output should be reviewed before following it, especially when a user has pain, an injury, a medical condition, is pregnant, or is returning to exercise after a medical issue.
