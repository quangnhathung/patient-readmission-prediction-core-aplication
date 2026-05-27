from datetime import datetime, timezone
from typing import Optional

import numpy as np
import pandas as pd

from app.core.exceptions import PredictionError, PreprocessingError
from app.core.logging_ import logger
from app.models.registry import ModelRegistry
from app.schemas.predict import PatientData, SinglePredictionResponse


class PredictionService:
    def __init__(self, registry: ModelRegistry):
        self._registry = registry

    def _df_from_patient(self, data: PatientData) -> pd.DataFrame:
        raw = data.model_dump(by_alias=True)
        return pd.DataFrame([raw])

    def predict_random_forest(self, data: PatientData, threshold: Optional[float] = None) -> SinglePredictionResponse:
        import time
        start = time.time()
        model_info = self._registry.get_model("random-forest")
        try:
            df = self._df_from_patient(data)
            processed = model_info.preprocessor.preprocess(df)
            proba = model_info.model.predict_proba(processed)[:, 1][0]
            thresh = threshold if threshold is not None else 0.2
            pred = int(proba >= thresh)
            elapsed = (time.time() - start) * 1000
            return SinglePredictionResponse(
                prediction=pred,
                probability=round(float(proba), 6),
                model_name=model_info.display_name,
                model_version=model_info.version,
                threshold=thresh,
                timestamp=datetime.now(timezone.utc).isoformat(),
                status="success",
                processing_time_ms=round(elapsed, 2),
            )
        except Exception as e:
            logger.error(f"Random Forest prediction failed: {e}")
            raise PredictionError("random-forest", str(e))

    def predict_xgboost(self, data: PatientData, threshold: Optional[float] = None) -> SinglePredictionResponse:
        import time
        start = time.time()
        model_info = self._registry.get_model("xgboost")
        try:
            df = self._df_from_patient(data)
            processed = model_info.preprocessor.preprocess(df)

            xgb_model = model_info.model["xgb"]
            lgb_model = model_info.model["lgb"]
            meta = model_info.model["meta"]

            xgb_proba = xgb_model.predict_proba(processed)[:, 1][0]
            lgb_proba = lgb_model.predict_proba(processed)[:, 1][0]

            xgb_w = meta.get("xgb_weight", 0.95)
            lgb_w = meta.get("lgb_weight", 0.05)
            ensemble_proba = xgb_w * xgb_proba + lgb_w * lgb_proba

            thresh = threshold if threshold is not None else meta.get("optimal_threshold_f2", 0.094)
            pred = int(ensemble_proba >= thresh)

            elapsed = (time.time() - start) * 1000
            return SinglePredictionResponse(
                prediction=pred,
                probability=round(float(ensemble_proba), 6),
                model_name=model_info.display_name,
                model_version=model_info.version,
                threshold=float(thresh),
                timestamp=datetime.now(timezone.utc).isoformat(),
                status="success",
                processing_time_ms=round(elapsed, 2),
            )
        except Exception as e:
            logger.error(f"XGBoost prediction failed: {e}")
            raise PredictionError("xgboost", str(e))

    def predict_ensemble(self, data: PatientData) -> SinglePredictionResponse:
        import time
        start = time.time()
        try:
            rf_resp = self.predict_random_forest(data, threshold=0.2)
            xgb_resp = self.predict_xgboost(data)

            probas = [rf_resp.probability, xgb_resp.probability]
            avg_proba = float(np.mean(probas))
            thresh = 0.2
            pred = int(avg_proba >= thresh)

            elapsed = (time.time() - start) * 1000
            return SinglePredictionResponse(
                prediction=pred,
                probability=avg_proba,
                model_name="Ensemble (Random Forest + XGBoost)",
                model_version="1.0",
                threshold=thresh,
                timestamp=datetime.now(timezone.utc).isoformat(),
                status="success",
                processing_time_ms=round(elapsed, 2),
            )
        except Exception as e:
            logger.error(f"Ensemble prediction failed: {e}")
            raise PredictionError("ensemble", str(e))

    def predict_batch(self, patients: list[PatientData], model_name: str, threshold: Optional[float] = None) -> tuple:
        import time
        start = time.time()
        predict_fn = {
            "random-forest": self.predict_random_forest,
            "xgboost": self.predict_xgboost,
            "ensemble": self.predict_ensemble,
        }
        if model_name not in predict_fn:
            raise PredictionError(model_name, f"Unsupported model: {model_name}")

        results = []
        for patient in patients:
            try:
                resp = predict_fn[model_name](patient, threshold)
                results.append(resp)
            except Exception as e:
                elapsed = (time.time() - start) * 1000
                results.append(SinglePredictionResponse(
                    prediction=-1,
                    probability=0.0,
                    model_name=model_name,
                    model_version="unknown",
                    threshold=threshold or 0.5,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    status=f"error: {str(e)}",
                    processing_time_ms=round(elapsed, 2),
                ))

        success_count = sum(1 for r in results if r.status == "success")
        return results, success_count
