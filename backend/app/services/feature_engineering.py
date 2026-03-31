import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "monthly_revenue",
    "active_users",
    "support_tickets",
    "last_login_days_ago",
    "contract_value",
    "tenure_months",
]
CAT_FEATURES = ["industry", "region"]
TARGET = "churned"


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["monthly_revenue"] = cleaned["monthly_revenue"].astype(float)
    cleaned["contract_value"] = cleaned["contract_value"].astype(float)
    cleaned["active_users"] = cleaned["active_users"].astype(int)
    cleaned["support_tickets"] = cleaned["support_tickets"].astype(int)
    cleaned["last_login_days_ago"] = cleaned["last_login_days_ago"].astype(int)
    cleaned["tenure_months"] = cleaned["tenure_months"].astype(int)
    cleaned["churned"] = cleaned["churned"].astype(int)
    return cleaned


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_FEATURES),
        ]
    )


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    return df[NUMERIC_FEATURES + CAT_FEATURES], df[TARGET]
