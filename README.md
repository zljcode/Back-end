# Demo Back-end

Minimal FastAPI backend scaffold for the visitor-risk demo.

## Structure

- `app/main.py`: FastAPI application entry
- `app/api/routes/health.py`: basic health route
- `requirements.txt`: Python dependencies

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

