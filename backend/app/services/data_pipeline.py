from pathlib import Path

import pandas as pd
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.business_record import BusinessRecord
from app.services.feature_engineering import prepare_dataframe


def load_raw_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return prepare_dataframe(df)


def ingest_dataframe(df: pd.DataFrame, db: Session) -> int:
    db.execute(delete(BusinessRecord))

    records = [
        BusinessRecord(
            customer_id=int(row["customer_id"]),
            company_name=str(row["company_name"]),
            industry=str(row["industry"]),
            region=str(row["region"]),
            monthly_revenue=float(row["monthly_revenue"]),
            active_users=int(row["active_users"]),
            support_tickets=int(row["support_tickets"]),
            last_login_days_ago=int(row["last_login_days_ago"]),
            contract_value=float(row["contract_value"]),
            tenure_months=int(row["tenure_months"]),
            churned=int(row["churned"]),
        )
        for _, row in df.iterrows()
    ]

    db.add_all(records)
    db.commit()
    return len(records)


def fetch_training_frame(db: Session) -> pd.DataFrame:
    rows = db.query(BusinessRecord).all()
    data = [
        {
            "customer_id": row.customer_id,
            "company_name": row.company_name,
            "industry": row.industry,
            "region": row.region,
            "monthly_revenue": row.monthly_revenue,
            "active_users": row.active_users,
            "support_tickets": row.support_tickets,
            "last_login_days_ago": row.last_login_days_ago,
            "contract_value": row.contract_value,
            "tenure_months": row.tenure_months,
            "churned": row.churned,
        }
        for row in rows
    ]
    return pd.DataFrame(data)
