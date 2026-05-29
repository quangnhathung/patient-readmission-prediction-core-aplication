import json
from pathlib import Path

import joblib

from .logger import setup_logger

logger = setup_logger(__name__)


def save_model(model, path: Path, name: str = "model"):
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    logger.info(f"Saved {name}: {path}")
    return str(path)


def load_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)


def save_metadata_json(metadata: dict, path: Path, name: str = "metadata"):
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {}
    for k, v in metadata.items():
        if isinstance(v, Path):
            serializable[k] = str(v)
        elif hasattr(v, "__dict__"):
            serializable[k] = str(v)
        else:
            serializable[k] = v
    with open(path, "w") as f:
        json.dump(serializable, f, indent=2, default=str)
    logger.info(f"Saved {name}: {path}")
    return str(path)


def save_all_artifacts(
    model,
    preprocessor,
    calibrated_model,
    schema,
    feature_metadata,
    best_params,
    train_metrics,
    val_metrics,
    cal_metrics,
    threshold_info,
    config,
    model_dir: str,
    output_dir: str,
):
    model_path = Path(model_dir)
    output_path = Path(output_dir)
    model_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    artifacts = {}

    artifacts["model"] = save_model(model, model_path / "random_forest_v2.joblib", "RF model")
    save_model(preprocessor, model_path / "preprocessor_v2.joblib", "preprocessor")

    if calibrated_model is not None:
        artifacts["calibrated_model"] = save_model(
            calibrated_model, model_path / "calibrated_rf_v2.joblib", "calibrated RF model"
        )

    artifacts["schema"] = save_metadata_json(schema, model_path / "model_schema_v2.json", "schema")
    artifacts["feature_metadata"] = save_metadata_json(
        feature_metadata, model_path / "feature_metadata_v2.json", "feature_metadata"
    )
    artifacts["best_params"] = save_metadata_json(
        best_params, model_path / "best_params_v2.json", "best_params"
    )

    all_metrics = {}
    if train_metrics:
        all_metrics.update(train_metrics)
    if val_metrics:
        all_metrics.update(val_metrics)
    if cal_metrics:
        all_metrics.update(cal_metrics)
    if threshold_info:
        all_metrics.update({f"threshold_{k}": v for k, v in threshold_info.items()})

    artifacts["metrics"] = save_metadata_json(all_metrics, output_path / "metrics_v2.json", "metrics")
    artifacts["training_config"] = save_metadata_json(config, model_path / "training_config_v2.json", "training config")

    logger.info("All artifacts saved successfully.")
    return artifacts
