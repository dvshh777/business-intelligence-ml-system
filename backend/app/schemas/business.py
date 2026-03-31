from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    industry: str
    region: str
    monthly_revenue: float = Field(gt=0)
    active_users: int = Field(gt=0)
    support_tickets: int = Field(ge=0)
    last_login_days_ago: int = Field(ge=0)
    contract_value: float = Field(gt=0)
    tenure_months: int = Field(gt=0)


class PredictionResponse(BaseModel):
    churn_risk: float
    predicted_label: int


class TrainingResponse(BaseModel):
    status: str
    metrics: dict[str, float]


class DashboardSummary(BaseModel):
    total_customers: int
    monthly_revenue: float
    avg_contract_value: float
    churn_rate: float
    at_risk_customers: int
