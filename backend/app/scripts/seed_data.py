from pathlib import Path

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.services.data_pipeline import ingest_dataframe, load_raw_csv


def main() -> None:
    Base.metadata.create_all(bind=engine)
    csv_path = Path(__file__).resolve().parents[3] / "data" / "raw" / "business_data.csv"
    df = load_raw_csv(csv_path)
    with SessionLocal() as db:
        inserted = ingest_dataframe(df, db)
    print(f"Inserted {inserted} rows into business_records.")


if __name__ == "__main__":
    main()
