from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BusinessRecord(Base):
    __tablename__ = "business_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255))
    industry: Mapped[str] = mapped_column(String(120), index=True)
    region: Mapped[str] = mapped_column(String(120), index=True)
    monthly_revenue: Mapped[float] = mapped_column(Float)
    active_users: Mapped[int] = mapped_column(Integer)
    support_tickets: Mapped[int] = mapped_column(Integer)
    last_login_days_ago: Mapped[int] = mapped_column(Integer)
    contract_value: Mapped[float] = mapped_column(Float)
    tenure_months: Mapped[int] = mapped_column(Integer)
    churned: Mapped[int] = mapped_column(Integer, index=True)
