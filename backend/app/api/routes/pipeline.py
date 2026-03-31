from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.data_pipeline import ingest_dataframe, load_raw_csv


router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/seed")
def seed_pipeline(db: Session = Depends(get_db)) -> dict[str, int]:
    csv_path = Path(__file__).resolve().parents[4] / "data" / "raw" / "business_data.csv"
    df = load_raw_csv(csv_path)
    inserted = ingest_dataframe(df, db)
    return {"inserted_rows": inserted}
