from ..utils.logger import setup_logger
from ..utils.metrics import find_optimal_threshold

logger = setup_logger(__name__)


def optimize_threshold(y_true, y_proba, config: dict):
    threshold_cfg = config.get("threshold", {})
    if not threshold_cfg.get("optimization", True):
        logger.info("Threshold optimization disabled, using default 0.5")
        return {"threshold": 0.5, "score": None, "method": "default"}

    metric = threshold_cfg.get("metric", "f1")
    min_t = threshold_cfg.get("min_threshold", 0.01)
    max_t = threshold_cfg.get("max_threshold", 0.99)
    step = threshold_cfg.get("step", 0.01)

    logger.info(f"Optimizing threshold for metric='{metric}'...")
    best_threshold, best_score = find_optimal_threshold(
        y_true, y_proba, metric=metric, min_t=min_t, max_t=max_t, step=step,
    )

    logger.info(f"Optimal threshold ({metric}): {best_threshold:.4f} (score: {best_score:.4f})")

    result = {
        "threshold": best_threshold,
        "score": best_score,
        "method": f"{metric}_optimization",
    }

    return result
