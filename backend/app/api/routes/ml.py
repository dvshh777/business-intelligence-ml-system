from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.business import PredictionRequest, PredictionResponse, TrainingResponse
from app.services.model_service import predict, train_model


router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/train", response_model=TrainingResponse)
def run_training(db: Session = Depends(get_db)) -> TrainingResponse:
    try:
        metrics = train_model(db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TrainingResponse(status="trained", metrics=metrics)


@router.post("/predict", response_model=PredictionResponse)
def predict_churn(payload: PredictionRequest) -> PredictionResponse:
    try:
        result = predict(payload.model_dump())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return PredictionResponse(**result)
