# Digital Tea Garden (scaffold)

End-to-end skeleton for the digital tea garden demo:
- **backend/** FastAPI service with mock data for plots, sensor readings, advice, disease upload, chat stub, stats.
- **frontend-uni/** uni-app project (WeChat Mini Program + H5) with core pages: overview, plot detail, disease diagnosis, stats, chat.
- **ml/** placeholder training area.
- **docs/** draft specs and plans.

## Run backend
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Uploads will land in `uploads/`. Mock data drives responses until DB/model integrations are added.

## Run frontend (HBuilderX / CLI)
Open `frontend-uni` with HBuilderX or your uni-app workflow, ensure `common/http.js` points to the backend URL (default `http://localhost:8000`), and run the Mini Program or H5 preview.
