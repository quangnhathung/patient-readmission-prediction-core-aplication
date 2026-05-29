import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    average_precision_score,
    classification_report,
    brier_score_loss,
)


def compute_all_metrics(y_true, y_pred, y_proba=None, prefix=""):
    metrics = {}
    metrics[f"{prefix}accuracy"] = float(accuracy_score(y_true, y_pred))
    metrics[f"{prefix}precision"] = float(precision_score(y_true, y_pred, zero_division=0))
    metrics[f"{prefix}recall"] = float(recall_score(y_true, y_pred, zero_division=0))
    metrics[f"{prefix}f1"] = float(f1_score(y_true, y_pred, zero_division=0))

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    metrics[f"{prefix}true_negatives"] = int(tn)
    metrics[f"{prefix}false_positives"] = int(fp)
    metrics[f"{prefix}false_negatives"] = int(fn)
    metrics[f"{prefix}true_positives"] = int(tp)

    if y_proba is not None:
        try:
            metrics[f"{prefix}roc_auc"] = float(roc_auc_score(y_true, y_proba))
        except Exception:
            metrics[f"{prefix}roc_auc"] = None
        try:
            metrics[f"{prefix}pr_auc"] = float(average_precision_score(y_true, y_proba))
        except Exception:
            metrics[f"{prefix}pr_auc"] = None
        try:
            metrics[f"{prefix}brier_score"] = float(brier_score_loss(y_true, y_proba))
        except Exception:
            metrics[f"{prefix}brier_score"] = None

    return metrics


def find_optimal_threshold(y_true, y_proba, metric="f1", min_t=0.01, max_t=0.99, step=0.01):
    thresholds = np.arange(min_t, max_t + step, step)
    best_score = 0.0
    best_threshold = 0.5

    for t in thresholds:
        y_pred = (y_proba >= t).astype(int)
        if metric == "f1":
            score = f1_score(y_true, y_pred, zero_division=0)
        elif metric == "youden":
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            tnr = tn / (tn + fp) if (tn + fp) > 0 else 0
            score = tpr + tnr - 1
        elif metric == "recall":
            score = recall_score(y_true, y_pred, zero_division=0)
        else:
            score = f1_score(y_true, y_pred, zero_division=0)

        if score > best_score:
            best_score = score
            best_threshold = float(t)

    return best_threshold, float(best_score)
