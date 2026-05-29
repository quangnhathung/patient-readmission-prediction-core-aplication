from sklearn.calibration import CalibratedClassifierCV

from ..utils.logger import setup_logger
from ..utils.metrics import compute_all_metrics

logger = setup_logger(__name__)


def calibrate_model(model, X_val, y_val, method="isotonic", cv_folds=5):
    logger.info(f"Calibrating model with method='{method}', cv={cv_folds}...")

    calibrator = CalibratedClassifierCV(
        estimator=model,
        method=method,
        cv=cv_folds,
        n_jobs=-1,
    )

    calibrator.fit(X_val, y_val)

    cal_proba = calibrator.predict_proba(X_val)[:, 1]
    cal_preds = calibrator.predict(X_val)

    metrics = compute_all_metrics(y_val, cal_preds, cal_proba, prefix="cal_")
    logger.info(f"Calibration metrics (val): F1={metrics.get('cal_f1', 0):.4f}, "
                f"ROC-AUC={metrics.get('cal_roc_auc', 0):.4f}, "
                f"Brier={metrics.get('cal_brier_score', 0):.4f}")

    result = {
        "calibrated_model": calibrator,
        "method": method,
        "metrics": metrics,
    }

    return result
