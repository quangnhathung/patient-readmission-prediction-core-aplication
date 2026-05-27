from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field("healthy", description="Service health status")
    version: str = Field(description="API version")
    models_loaded: int = Field(description="Number of loaded models")
    models: list[str] = Field(description="List of available model names")
    uptime_seconds: float = Field(description="Service uptime in seconds")


class ModelMetadataResponse(BaseModel):
    name: str
    display_name: str
    description: str
    version: str
    model_type: str
    metadata: dict
    feature_count: int


class ModelListResponse(BaseModel):
    models: dict[str, ModelMetadataResponse]
    total: int
