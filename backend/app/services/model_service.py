import json

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.services.data_pipeline import fetch_training_frame
from app.services.feature_engineering import build_preprocessor, split_features_target


settings = get_settings()


def train_model(db: Session) -> dict[str, float]:
    df = fetch_training_frame(db)
    if df.empty:
        raise ValueError("No training data found in database.")

    x, y = split_features_target(df)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y if y.nunique() > 1 else None,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", build_preprocessor()),
            ("model", RandomForestClassifier(n_estimators=200, random_state=42)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
    }

    settings.resolved_model_path.parent.mkdir(parents=True, exist_ok=True)
    settings.resolved_metrics_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, settings.resolved_model_path)
    settings.resolved_metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def load_model() -> Pipeline:
    if not settings.resolved_model_path.exists():
        raise FileNotFoundError("Model artifact not found. Train the model first.")
    return joblib.load(settings.resolved_model_path)


def load_metrics() -> dict[str, float]:
    if not settings.resolved_metrics_path.exists():
        return {}
    return json.loads(settings.resolved_metrics_path.read_text(encoding="utf-8"))


def predict(payload: dict) -> dict[str, float | int]:
    model = load_model()
    frame = pd.DataFrame([payload])
    probabilities = model.predict_proba(frame)[0]
    predicted_label = int(model.predict(frame)[0])
    return {
        "churn_risk": round(float(probabilities[1] if len(probabilities) > 1 else probabilities[0]), 4),
        "predicted_label": predicted_label,
    }
