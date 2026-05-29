import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay,
    classification_report,
)

from ..utils.logger import setup_logger
from ..utils.metrics import compute_all_metrics

logger = setup_logger(__name__)

plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
})


class Evaluator:
    def __init__(self, report_dir: str):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def evaluate(self, y_true, y_pred, y_proba, prefix="") -> dict:
        return compute_all_metrics(y_true, y_pred, y_proba, prefix=prefix)

    def plot_confusion_matrix(self, y_true, y_pred, title="Confusion Matrix", filename="confusion_matrix.png"):
        fig, ax = plt.subplots(figsize=(6, 5))
        ConfusionMatrixDisplay.from_predictions(
            y_true, y_pred,
            display_labels=["Low Risk (0)", "High Risk (1)"],
            cmap="Blues",
            ax=ax,
            colorbar=False,
            values_format="d",
        )
        ax.set_title(title)
        for text in ax.texts:
            text.set_fontsize(14)
        plt.tight_layout()
        path = self.report_dir / filename
        plt.savefig(path)
        plt.close()
        logger.info(f"Saved: {path}")
        return str(path)

    def plot_roc_curve(self, y_true, y_proba, title="ROC Curve", filename="roc_curve.png"):
        fig, ax = plt.subplots(figsize=(7, 6))
        RocCurveDisplay.from_predictions(y_true, y_proba, ax=ax)
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random")
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()
        path = self.report_dir / filename
        plt.savefig(path)
        plt.close()
        logger.info(f"Saved: {path}")
        return str(path)

    def plot_pr_curve(self, y_true, y_proba, title="Precision-Recall Curve", filename="pr_curve.png"):
        fig, ax = plt.subplots(figsize=(7, 6))
        PrecisionRecallDisplay.from_predictions(y_true, y_proba, ax=ax)
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()
        path = self.report_dir / filename
        plt.savefig(path)
        plt.close()
        logger.info(f"Saved: {path}")
        return str(path)

    def plot_feature_importance(self, feature_names, importances, top_n=30, title="Feature Importance", filename="feature_importance.png"):
        indices = np.argsort(importances)[::-1][:top_n]
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(len(indices)), importances[indices][::-1], align="center")
        ax.set_yticks(range(len(indices)))
        ax.set_yticklabels([feature_names[i] for i in indices[::-1]], fontsize=8)
        ax.set_xlabel("Importance")
        ax.set_title(title)
        plt.tight_layout()
        path = self.report_dir / filename
        plt.savefig(path)
        plt.close()
        logger.info(f"Saved: {path}")
        return str(path)

    def plot_calibration_curve(self, y_true, y_proba_uncal, y_proba_cal=None, title="Calibration Curve", filename="calibration_curve.png"):
        fig, ax = plt.subplots(figsize=(7, 6))
        prob_true_uncal, prob_pred_uncal = calibration_curve(y_true, y_proba_uncal, n_bins=10)
        ax.plot(prob_pred_uncal, prob_true_uncal, "s-", label="Uncalibrated", markersize=6)
        if y_proba_cal is not None:
            prob_true_cal, prob_pred_cal = calibration_curve(y_true, y_proba_cal, n_bins=10)
            ax.plot(prob_pred_cal, prob_true_cal, "o-", label="Calibrated", markersize=6)
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfectly Calibrated")
        ax.set_xlabel("Mean Predicted Probability")
        ax.set_ylabel("Fraction of Positives")
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()
        path = self.report_dir / filename
        plt.savefig(path)
        plt.close()
        logger.info(f"Saved: {path}")
        return str(path)

    def plot_threshold_analysis(self, y_true, y_proba, filename="threshold_analysis.png"):
        thresholds = np.arange(0.01, 0.99, 0.02)
        precisions, recalls, f1s = [], [], []
        for t in thresholds:
            y_pred = (y_proba >= t).astype(int)
            m = compute_all_metrics(y_true, y_pred, y_proba)
            precisions.append(m.get("precision", 0))
            recalls.append(m.get("recall", 0))
            f1s.append(m.get("f1", 0))

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(thresholds, precisions, label="Precision", linewidth=2)
        ax.plot(thresholds, recalls, label="Recall", linewidth=2)
        ax.plot(thresholds, f1s, label="F1-Score", linewidth=2)
        ax.set_xlabel("Threshold")
        ax.set_ylabel("Score")
        ax.set_title("Threshold Analysis")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        path = self.report_dir / filename
        plt.savefig(path)
        plt.close()
        logger.info(f"Saved: {path}")
        return str(path)

    def save_classification_report(self, y_true, y_pred, filename="classification_report.txt"):
        report = classification_report(
            y_true, y_pred,
            target_names=["Low Risk (0)", "High Risk (1)"],
            digits=4,
        )
        path = self.report_dir / filename
        with open(path, "w") as f:
            f.write(report)
        logger.info(f"Saved: {path}")
        return report

    def save_metrics_json(self, metrics: dict, filename="metrics.json"):
        serializable = {}
        for k, v in metrics.items():
            if isinstance(v, (np.integer,)):
                serializable[k] = int(v)
            elif isinstance(v, (np.floating,)):
                serializable[k] = float(v)
            elif isinstance(v, np.ndarray):
                serializable[k] = v.tolist()
            else:
                serializable[k] = v
        path = self.report_dir / filename
        with open(path, "w") as f:
            json.dump(serializable, f, indent=2, default=str)
        logger.info(f"Saved: {path}")
        return str(path)

    def save_metrics_csv(self, metrics: dict, filename="metrics.csv"):
        flat = {}
        for k, v in metrics.items():
            if isinstance(v, (int, float, str, np.integer, np.floating)):
                flat[k] = v
        df = pd.DataFrame([flat])
        path = self.report_dir / filename
        df.to_csv(path, index=False)
        logger.info(f"Saved: {path}")
        return str(path)
