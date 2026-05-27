import time

from fastapi import APIRouter, Request

from app.core.config import settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])

_start_time = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    description="Returns the health status of the API, including loaded models and uptime.",
)
async def health(request: Request):
    registry = request.app.state.model_registry
    uptime = time.time() - _start_time
    return HealthResponse(
        status="healthy",
        version=settings.project_version,
        models_loaded=len(registry.available_models),
        models=registry.available_models,
        uptime_seconds=round(uptime, 2),
    )


@router.get(
    "/version",
    summary="Get API version",
    description="Returns the current API version information.",
)
async def version():
    return {
        "project_name": settings.project_name,
        "version": settings.project_version,
        "api_prefix": settings.api_v1_prefix,
    }
