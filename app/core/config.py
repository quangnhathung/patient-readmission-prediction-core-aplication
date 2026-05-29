from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Hospital Readmission Prediction API"
    project_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    log_level: str = "INFO"
    log_format: str = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"

    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    random_forest_model_path: Path = base_dir / "RandomForest" / "readmission_rf" / "outputs" / "best_rf_model.pkl"
    random_forest_v2_model_path: Path = base_dir / "RandomForest" / "models" / "random_forest_v2.joblib"
    random_forest_v2_calibrated_path: Path = base_dir / "RandomForest" / "models" / "calibrated_rf_v2.joblib"
    random_forest_v2_preprocessor_path: Path = base_dir / "RandomForest" / "models" / "preprocessor_v2.joblib"
    random_forest_v2_schema_path: Path = base_dir / "RandomForest" / "models" / "model_schema_v2.json"
    random_forest_v2_metrics_path: Path = base_dir / "RandomForest" / "outputs" / "metrics_v2.json"

    xgboost_model_path: Path = base_dir / "xgBoost" / "models" / "calibrated_xgb_v3.joblib"
    xgboost_lgbm_path: Path = base_dir / "xgBoost" / "models" / "calibrated_lgb_v3.joblib"
    xgboost_ensemble_meta_path: Path = base_dir / "xgBoost" / "models" / "ensemble_meta_v3.json"
    xgboost_schema_path: Path = base_dir / "xgBoost" / "models" / "model_schema_v3.json"

    model_cache_ttl_seconds: int = 3600

    default_threshold: float = 0.5

    class Config:
        env_file: ClassVar[str] = ".env"
        env_file_encoding: ClassVar[str] = "utf-8"


settings = Settings()
