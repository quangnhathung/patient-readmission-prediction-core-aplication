from fastapi import Depends, Request

from app.models.registry import ModelRegistry
from app.services.prediction import PredictionService


def get_registry(request: Request) -> ModelRegistry:
    registry: ModelRegistry = request.app.state.model_registry
    return registry


def get_prediction_service(registry: ModelRegistry = Depends(get_registry)) -> PredictionService:
    return PredictionService(registry)
