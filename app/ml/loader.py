import json
from pathlib import Path
from typing import Any, Optional

import joblib


def load_pickle(path: Path) -> Any:
    return joblib.load(path)


def load_joblib(path: Path) -> Any:
    return joblib.load(path)


def load_json(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def load_model(path: Path) -> Any:
    suffix = path.suffix.lower()
    if suffix in (".pkl", ".pickle"):
        return load_pickle(path)
    if suffix in (".joblib",):
        return load_joblib(path)
    if suffix in (".json",):
        return load_json(path)
    raise ValueError(f"Unsupported model format: {suffix}")


def get_feature_names(model: Any) -> Optional[list[str]]:
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    if hasattr(model, "feature_name_"):
        return model.feature_name_()
    if hasattr(model, "get_booster"):
        try:
            return model.get_booster().feature_names
        except Exception:
            pass
    return None
