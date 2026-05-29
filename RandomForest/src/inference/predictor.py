import numpy as np
import pandas as pd

from ..preprocessing.feature_engineering import build_features
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class RandomForestPredictor:
    def __init__(self, model, preprocessor, threshold=0.5, calibrated_model=None):
        self.model = model
        self.preprocessor = preprocessor
        self.threshold = threshold
        self.calibrated_model = calibrated_model

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        df_fe = build_features(df)
        X = self.preprocessor.transform(df_fe)
        if self.calibrated_model is not None:
            proba = self.calibrated_model.predict_proba(X)
        else:
            proba = self.model.predict_proba(X)
        return proba[:, 1]

    def predict(self, df: pd.DataFrame, threshold: float = None) -> np.ndarray:
        if threshold is None:
            threshold = self.threshold
        proba = self.predict_proba(df)
        return (proba >= threshold).astype(int)

    def predict_single(self, data: dict, threshold: float = None) -> dict:
        df = pd.DataFrame([data])
        proba = self.predict_proba(df)[0]
        if threshold is None:
            threshold = self.threshold
        pred = int(proba >= threshold)
        return {
            "prediction": pred,
            "probability": round(float(proba), 6),
            "threshold": threshold,
        }
