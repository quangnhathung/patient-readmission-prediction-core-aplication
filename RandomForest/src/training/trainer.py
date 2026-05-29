import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline

from ..preprocessing.pipline_builder import build_preprocessor
from ..preprocessing.feature_engineering import build_features
from ..utils.logger import setup_logger
from ..utils.metrics import compute_all_metrics

logger = setup_logger(__name__)


def train_random_forest(X_train, y_train, X_val, y_val, config: dict):
    tuning_cfg = config.get("tuning", {})
    model_cfg = config.get("model", {})

    if tuning_cfg.get("enabled", True):
        logger.info("Building preprocessing pipeline...")
        preprocessor, feature_metadata, trained_columns = build_preprocessor(X_train, config)

        logger.info("Transforming training data...")
        X_train_transformed = preprocessor.transform(build_features(X_train))
        X_val_transformed = preprocessor.transform(build_features(X_val))

        param_dist = tuning_cfg.get("param_distributions", {})
        n_iter = tuning_cfg.get("n_iter", 100)
        cv_folds = tuning_cfg.get("cv_folds", 5)
        scoring = tuning_cfg.get("scoring", "f1")
        n_jobs = tuning_cfg.get("n_jobs", -1)
        seed = config.get("seed", 42)

        rf_base = RandomForestClassifier(
            random_state=seed,
            n_jobs=1,
        )

        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=seed)

        logger.info(f"Starting RandomizedSearchCV with {n_iter} iterations, {cv_folds}-fold CV...")
        search = RandomizedSearchCV(
            estimator=rf_base,
            param_distributions=param_dist,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs,
            verbose=1,
            random_state=seed,
            return_train_score=True,
        )

        search.fit(X_train_transformed, y_train)

        best_rf = search.best_estimator_
        best_params = search.best_params_

        logger.info(f"Best CV score ({scoring}): {search.best_score_:.4f}")
        logger.info(f"Best params: {best_params}")

        train_preds = best_rf.predict(X_train_transformed)
        train_proba = best_rf.predict_proba(X_train_transformed)[:, 1]
        val_preds = best_rf.predict(X_val_transformed)
        val_proba = best_rf.predict_proba(X_val_transformed)[:, 1]

        train_metrics = compute_all_metrics(y_train, train_preds, train_proba, prefix="train_")
        val_metrics = compute_all_metrics(y_val, val_preds, val_proba, prefix="val_")

        overfitting_score = train_metrics.get("train_f1", 0) - val_metrics.get("val_f1", 0)
        logger.info(f"Train F1: {train_metrics.get('train_f1', 0):.4f}")
        logger.info(f"Val F1: {val_metrics.get('val_f1', 0):.4f}")
        logger.info(f"Overfitting gap (F1): {overfitting_score:.4f}")

        result = {
            "model": best_rf,
            "preprocessor": preprocessor,
            "best_params": best_params,
            "train_metrics": train_metrics,
            "val_metrics": val_metrics,
            "cv_results": {
                "best_score": float(search.best_score_),
                "best_params": best_params,
            },
            "feature_metadata": feature_metadata,
            "trained_columns": trained_columns,
            "overfitting_gap_f1": float(overfitting_score),
        }

        return result

    else:
        logger.info("Training without hyperparameter tuning...")

        preprocessor, feature_metadata, trained_columns = build_preprocessor(X_train, config)

        X_train_transformed = preprocessor.transform(build_features(X_train))
        X_val_transformed = preprocessor.transform(build_features(X_val))

        rf = RandomForestClassifier(
            n_estimators=model_cfg.get("n_estimators", 300),
            max_depth=model_cfg.get("max_depth", 15),
            min_samples_split=model_cfg.get("min_samples_split", 5),
            min_samples_leaf=model_cfg.get("min_samples_leaf", 2),
            class_weight=model_cfg.get("class_weight", "balanced"),
            random_state=model_cfg.get("random_state", config.get("seed", 42)),
            n_jobs=model_cfg.get("n_jobs", -1),
        )

        rf.fit(X_train_transformed, y_train)

        train_preds = rf.predict(X_train_transformed)
        train_proba = rf.predict_proba(X_train_transformed)[:, 1]
        val_preds = rf.predict(X_val_transformed)
        val_proba = rf.predict_proba(X_val_transformed)[:, 1]

        train_metrics = compute_all_metrics(y_train, train_preds, train_proba, prefix="train_")
        val_metrics = compute_all_metrics(y_val, val_preds, val_proba, prefix="val_")

        overfitting_score = train_metrics.get("train_f1", 0) - val_metrics.get("val_f1", 0)

        result = {
            "model": rf,
            "preprocessor": preprocessor,
            "best_params": rf.get_params(),
            "train_metrics": train_metrics,
            "val_metrics": val_metrics,
            "cv_results": None,
            "feature_metadata": feature_metadata,
            "trained_columns": trained_columns,
            "overfitting_gap_f1": float(overfitting_score),
        }

        return result
