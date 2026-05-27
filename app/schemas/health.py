from datetime import datetime, timezone

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field("healthy", description="Service health status")
    version: str = Field(description="API version")
    models_loaded: int = Field(description="Number of loaded models")
    models: list[str] = Field(description="List of available model names")
    uptime_seconds: float = Field(description="Service uptime in seconds")


class VersionResponse(BaseModel):
    project_name: str
    version: str
    api_prefix: str
