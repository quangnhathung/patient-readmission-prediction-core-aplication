from fastapi import APIRouter, Depends

from app.core.dependencies import get_registry
from app.models.registry import ModelRegistry
from app.schemas.metadata import ModelListResponse, ModelMetadataResponse

router = APIRouter(tags=["Models"])


@router.get(
    "/models",
    response_model=ModelListResponse,
    summary="List all loaded models",
    description="Returns metadata for all loaded machine learning models.",
)
async def list_models(registry: ModelRegistry = Depends(get_registry)):
    models_dict = {}
    for name in registry.available_models:
        info = registry.get_model(name)
        models_dict[name] = ModelMetadataResponse(
            name=info.name,
            display_name=info.display_name,
            description=info.description,
            version=info.version,
            model_type=info.model_type,
            metadata=info.metadata,
            feature_count=len(info.feature_columns) if info.feature_columns else 0,
        )
    return ModelListResponse(models=models_dict, total=len(models_dict))


@router.get(
    "/models/{model_name}",
    response_model=ModelMetadataResponse,
    summary="Get model metadata",
    description="Returns detailed metadata for a specific model.",
)
async def get_model_metadata(model_name: str, registry: ModelRegistry = Depends(get_registry)):
    info = registry.get_model(model_name)
    return ModelMetadataResponse(
        name=info.name,
        display_name=info.display_name,
        description=info.description,
        version=info.version,
        model_type=info.model_type,
        metadata=info.metadata,
        feature_count=len(info.feature_columns) if info.feature_columns else 0,
    )
