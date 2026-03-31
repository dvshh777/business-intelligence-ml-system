from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.business_record import BusinessRecord
from app.schemas.business import DashboardSummary
from app.services.model_service import load_metrics, load_model


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    total_customers = db.scalar(select(func.count(BusinessRecord.id))) or 0
    total_revenue = db.scalar(select(func.sum(BusinessRecord.monthly_revenue))) or 0.0
    avg_contract_value = db.scalar(select(func.avg(BusinessRecord.contract_value))) or 0.0
    churn_rate = db.scalar(select(func.avg(BusinessRecord.churned))) or 0.0

    at_risk = 0
    try:
        model = load_model()
        rows = db.query(BusinessRecord).all()
        if rows:
            import pandas as pd

            frame = pd.DataFrame(
                [
                    {
                        "industry": row.industry,
                        "region": row.region,
                        "monthly_revenue": row.monthly_revenue,
                        "active_users": row.active_users,
                        "support_tickets": row.support_tickets,
                        "last_login_days_ago": row.last_login_days_ago,
                        "contract_value": row.contract_value,
                        "tenure_months": row.tenure_months,
                    }
                    for row in rows
                ]
            )
            at_risk = int(sum(model.predict(frame)))
    except FileNotFoundError:
        at_risk = 0

    return DashboardSummary(
        total_customers=int(total_customers),
        monthly_revenue=round(float(total_revenue), 2),
        avg_contract_value=round(float(avg_contract_value), 2),
        churn_rate=round(float(churn_rate), 4),
        at_risk_customers=at_risk,
    )


@router.get("/model-metrics")
def get_model_metrics() -> dict[str, dict[str, float]]:
    return {"metrics": load_metrics()}
