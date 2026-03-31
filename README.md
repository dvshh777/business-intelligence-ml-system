# Business Intelligence ML System

An end-to-end starter project for a business intelligence platform with FastAPI, scikit-learn, React, and PostgreSQL.

## Structure

- `backend/`: API layer, ETL pipeline, model training, database integration
- `frontend/`: React dashboard
- `data/`: sample raw business dataset
- `artifacts/`: trained model outputs

## Core flow

1. Seed raw CSV data into PostgreSQL.
2. Train a churn-risk model with scikit-learn.
3. Serve analytics and predictions through FastAPI.
4. Visualize KPIs and trigger retraining from React.

## Quick start

```powershell
docker compose up -d db
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m app.scripts.seed_data
python -m app.scripts.train_model
uvicorn app.main:app --reload --port 8000
```

```powershell
cd frontend
npm install
npm run dev
```
