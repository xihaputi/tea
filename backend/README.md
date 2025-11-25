# Digital Tea Garden Backend (FastAPI)

Lightweight FastAPI service exposing core endpoints for the tea garden demo: plots, sensor data, irrigation advice, disease detection upload, chat stub, and stats.

## Quick start
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate  # or source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Use MySQL instead of SQLite
Set `DB_URL` (or `db_url`) in `backend/.env`, e.g.:
```
DB_URL=mysql+pymysql://user:password@localhost:3306/tea
```
Then start `uvicorn` as above. SQLite remains the fallback if `DB_URL` is not set.

## Folder layout
- `app/main.py` FastAPI entrypoint
- `app/routers/` Route handlers for each domain
- `app/services/` Business logic stubs (rule engine, model hooks)
- `app/utils/` Helpers (file saving, time)
- `uploads/` Upload destination (shared with project root)
