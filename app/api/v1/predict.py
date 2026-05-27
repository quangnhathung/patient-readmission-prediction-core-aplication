from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_prediction_service
from app.schemas.predict import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    PatientData,
    SinglePredictionResponse,
)
from app.services.prediction import PredictionService

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post(
    "/random-forest",
    response_model=SinglePredictionResponse,
    summary="Predict readmission using Random Forest",
    description="Predicts 30-day hospital readmission risk using the Random Forest model with ADASYN balancing and GridSearchCV tuning. Default threshold is 0.2 (recall-optimized).",
)
async def predict_random_forest(
    data: PatientData,
    threshold: Optional[float] = Query(None, ge=0.0, le=1.0, description="Custom classification threshold (default: 0.2)"),
    service: PredictionService = Depends(get_prediction_service),
):
    return service.predict_random_forest(data, threshold)


@router.post(
    "/xgboost",
    response_model=SinglePredictionResponse,
    summary="Predict readmission using XGBoost + LightGBM Ensemble",
    description="Predicts 30-day hospital readmission risk using the calibrated XGBoost + LightGBM ensemble with isotonic calibration. Uses feature engineering and native categorical support. Default threshold is the F2-optimal threshold from training.",
)
async def predict_xgboost(
    data: PatientData,
    threshold: Optional[float] = Query(None, ge=0.0, le=1.0, description="Custom classification threshold (default: F2-optimal threshold)"),
    service: PredictionService = Depends(get_prediction_service),
):
    return service.predict_xgboost(data, threshold)


@router.post(
    "/ensemble",
    response_model=SinglePredictionResponse,
    summary="Predict readmission using all models (Ensemble)",
    description="Averaged ensemble of Random Forest and XGBoost. Each model preprocesses features independently; final probability is the mean across models.",
)
async def predict_ensemble(
    data: PatientData,
    service: PredictionService = Depends(get_prediction_service),
):
    return service.predict_ensemble(data)


@router.post(
    "/batch",
    response_model=BatchPredictionResponse,
    summary="Batch prediction for multiple patients",
    description="Predict readmission risk for up to 1000 patients in a single request using the specified model.",
)
async def predict_batch(
    request: BatchPredictionRequest,
    model: str = Query("random-forest", description="Model to use: random-forest, xgboost, ensemble"),
    threshold: Optional[float] = Query(None, ge=0.0, le=1.0, description="Custom classification threshold"),
    service: PredictionService = Depends(get_prediction_service),
):
    results, success_count = service.predict_batch(request.patients, model, threshold)
    return BatchPredictionResponse(
        predictions=results,
        total_count=len(request.patients),
        success_count=success_count,
        model_name=model,
        timestamp=datetime.now(timezone.utc).isoformat(),
        status="success",
    )
