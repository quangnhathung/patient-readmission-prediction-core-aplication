import time

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import health, metadata, predict
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logging_ import logger, setup_logging
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.models.registry import ModelRegistry


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    registry = ModelRegistry()
    registry.load_all()
    app.state.model_registry = registry
    app.state.start_time = time.time()
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description="Production-ready REST API for predicting 30-day hospital readmission risk using Random Forest and XGBoost-LightGBM Ensemble.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)
app.add_middleware(RequestLoggingMiddleware)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_code": exc.error_code,
            "detail": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_code": "INTERNAL_ERROR",
            "detail": "An unexpected error occurred",
        },
    )


app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(metadata.router, prefix=settings.api_v1_prefix)
app.include_router(predict.router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["Root"])
async def root():
    return {
        "project": settings.project_name,
        "version": settings.project_version,
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health",
    }
