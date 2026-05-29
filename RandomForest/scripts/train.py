#!/usr/bin/env python3
"""
Random Forest v2 Training Script
Usage:
    python scripts/train.py --config configs/rf_v2.yaml
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.preprocessing.cleaner import load_and_clean_data
from src.preprocessing.feature_engineering import build_features
from src.training.trainer import train_random_forest
from src.training.calibration import calibrate_model
from src.training.threshold import optimize_threshold
from src.evaluation.evaluator import Evaluator
from src.inference.predictor import RandomForestPredictor
from src.inference.schema import generate_schema
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger
from src.utils.artifact_manager import save_all_artifacts


def main():
    parser = argparse.ArgumentParser(description="Train Random Forest v2 for Patient Readmission Prediction")
    parser.add_argument("--config", "-c", type=str, default="configs/rf_v2.yaml",
                        help="Path to configuration file (YAML/JSON)")
    args = parser.parse_args()

    config = load_config(args.config)
    seed = config.get("seed", 42)
    np.random.seed(seed)

    log_level = config.get("logging", {}).get("level", "INFO")
    log_format = config.get("logging", {}).get("format", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    logger = setup_logger("train", level=log_level, log_format=log_format)
    logger.info(f"Starting experiment: {config.get('experiment_name', 'rf_v2')}")
    logger.info(f"Config: {args.config}")

    logger.info("=" * 60)
    logger.info("STEP 1/8: Loading and cleaning data")
    logger.info("=" * 60)
    data_cfg = config.get("data", {})
    X, y = load_and_clean_data(
        data_path=data_cfg.get("path", "RandomForest/data/diabetic_data.csv"),
        target_col=data_cfg.get("target_col", "readmitted"),
        positive_class=data_cfg.get("positive_class", "<30"),
        drop_cols=data_cfg.get("drop_cols", ["encounter_id", "patient_nbr", "weight"]),
        exclude_discharge_ids=data_cfg.get("exclude_discharge_ids", [11, 13, 14, 19, 20, 21]),
        keep_first_encounter=data_cfg.get("keep_first_encounter", True),
    )
    pos_ratio = y.mean() * 100
    logger.info(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features")
    logger.info(f"Positive class ratio: {pos_ratio:.2f}%")

    logger.info("=" * 60)
    logger.info("STEP 2/8: Train/Validation/Test split")
    logger.info("=" * 60)
    test_size = config.get("test_size", 0.2)
    val_size = config.get("val_size", 0.2)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=seed,
    )
    val_relative_size = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=val_relative_size, stratify=y_train, random_state=seed,
    )

    logger.info(f"Train: {len(X_train)} samples ({y_train.mean()*100:.2f}% positive)")
    logger.info(f"Val:   {len(X_val)} samples ({y_val.mean()*100:.2f}% positive)")
    logger.info(f"Test:  {len(X_test)} samples ({y_test.mean()*100:.2f}% positive)")

    logger.info("=" * 60)
    logger.info("STEP 3/8: Training Random Forest with hyperparameter tuning")
    logger.info("=" * 60)
    train_result = train_random_forest(X_train, y_train, X_val, y_val, config)
    best_rf = train_result["model"]
    preprocessor = train_result["preprocessor"]
    best_params = train_result["best_params"]
    train_metrics = train_result["train_metrics"]
    val_metrics = train_result["val_metrics"]
    feature_metadata = train_result["feature_metadata"]
    trained_columns = train_result["trained_columns"]

    logger.info(f"Train F1: {train_metrics.get('train_f1', 0):.4f}")
    logger.info(f"Val F1:   {val_metrics.get('val_f1', 0):.4f}")
    logger.info(f"Val ROC-AUC: {val_metrics.get('val_roc_auc', 0):.4f}")
    logger.info(f"Val PR-AUC:  {val_metrics.get('val_pr_auc', 0):.4f}")

    logger.info("=" * 60)
    logger.info("STEP 4/8: Probability Calibration")
    logger.info("=" * 60)
    cal_cfg = config.get("calibration", {})
    cal_result = None
    cal_metrics = None
    calibrated_model = None
    if cal_cfg.get("enabled", True):
        X_val_fe = build_features(X_val)
        X_val_transformed = preprocessor.transform(X_val_fe)
        cal_result = calibrate_model(
            best_rf, X_val_transformed, y_val,
            method=cal_cfg.get("method", "isotonic"),
            cv_folds=cal_cfg.get("cv_folds", 5),
        )
        calibrated_model = cal_result["calibrated_model"]
        cal_metrics = cal_result["metrics"]
    else:
        logger.info("Calibration disabled.")

    logger.info("=" * 60)
    logger.info("STEP 5/8: Threshold Optimization")
    logger.info("=" * 60)
    X_val_fe = build_features(X_val)
    X_val_transformed = preprocessor.transform(X_val_fe)
    val_proba = (
        calibrated_model.predict_proba(X_val_transformed)[:, 1]
        if calibrated_model is not None
        else best_rf.predict_proba(X_val_transformed)[:, 1]
    )
    threshold_result = optimize_threshold(y_val, val_proba, config)
    optimal_threshold = threshold_result["threshold"]

    logger.info("=" * 60)
    logger.info("STEP 6/8: Test Set Evaluation")
    logger.info("=" * 60)
    report_dir = config.get("output", {}).get("report_dir", "RandomForest/reports")
    evaluator = Evaluator(report_dir)

    X_test_fe = build_features(X_test)
    X_test_transformed = preprocessor.transform(X_test_fe)
    test_proba = (
        calibrated_model.predict_proba(X_test_transformed)[:, 1]
        if calibrated_model is not None
        else best_rf.predict_proba(X_test_transformed)[:, 1]
    )
    test_preds_optimal = (test_proba >= optimal_threshold).astype(int)
    test_preds_default = (test_proba >= 0.5).astype(int)

    test_metrics_optimal = evaluator.evaluate(y_test, test_preds_optimal, test_proba, prefix="test_optimal_")
    test_metrics_default = evaluator.evaluate(y_test, test_preds_default, test_proba, prefix="test_default_")

    logger.info(f"Test (optimal threshold={optimal_threshold:.4f}):")
    logger.info(f"  Accuracy:  {test_metrics_optimal.get('test_optimal_accuracy', 0):.4f}")
    logger.info(f"  Precision: {test_metrics_optimal.get('test_optimal_precision', 0):.4f}")
    logger.info(f"  Recall:    {test_metrics_optimal.get('test_optimal_recall', 0):.4f}")
    logger.info(f"  F1:        {test_metrics_optimal.get('test_optimal_f1', 0):.4f}")
    logger.info(f"  ROC-AUC:   {test_metrics_optimal.get('test_optimal_roc_auc', 0):.4f}")
    logger.info(f"  PR-AUC:    {test_metrics_optimal.get('test_optimal_pr_auc', 0):.4f}")
    logger.info(f"  FN:        {test_metrics_optimal.get('test_optimal_false_negatives', 0)}")

    logger.info(f"Test (default threshold=0.50):")
    logger.info(f"  Accuracy:  {test_metrics_default.get('test_default_accuracy', 0):.4f}")
    logger.info(f"  Precision: {test_metrics_default.get('test_default_precision', 0):.4f}")
    logger.info(f"  Recall:    {test_metrics_default.get('test_default_recall', 0):.4f}")
    logger.info(f"  F1:        {test_metrics_default.get('test_default_f1', 0):.4f}")

    logger.info("=" * 60)
    logger.info("STEP 7/8: Generating Charts and Reports")
    logger.info("=" * 60)

    evaluator.plot_confusion_matrix(
        y_test, test_preds_optimal,
        title=f"Confusion Matrix (threshold={optimal_threshold:.3f})",
        filename="confusion_matrix.png",
    )
    evaluator.plot_roc_curve(y_test, test_proba, filename="roc_curve.png")
    evaluator.plot_pr_curve(y_test, test_proba, filename="pr_curve.png")

    if hasattr(best_rf, "feature_importances_"):
        feature_names = list(X_test_transformed.columns) if hasattr(X_test_transformed, "columns") else [
            f"feature_{i}" for i in range(X_test_transformed.shape[1])
        ]
        evaluator.plot_feature_importance(
            feature_names, best_rf.feature_importances_,
            filename="feature_importance.png",
        )

    if cal_result is not None:
        uncal_proba = best_rf.predict_proba(X_test_transformed)[:, 1]
        evaluator.plot_calibration_curve(
            y_test, uncal_proba, test_proba,
            filename="calibration_curve.png",
        )

    evaluator.plot_threshold_analysis(y_test, test_proba, filename="threshold_analysis.png")

    report_text = evaluator.save_classification_report(y_test, test_preds_optimal, filename="classification_report.txt")
    print("\n" + report_text)

    all_metrics = {}
    all_metrics.update(train_metrics)
    all_metrics.update(val_metrics)
    if cal_metrics:
        all_metrics.update(cal_metrics)
    all_metrics.update(test_metrics_optimal)
    all_metrics.update(test_metrics_default)
    all_metrics["optimal_threshold"] = optimal_threshold
    all_metrics["threshold_optimization_method"] = threshold_result.get("method", "unknown")

    evaluator.save_metrics_json(all_metrics, filename="metrics.json")
    evaluator.save_metrics_csv(all_metrics, filename="metrics.csv")

    logger.info("=" * 60)
    logger.info("STEP 8/8: Saving Artifacts")
    logger.info("=" * 60)

    schema = generate_schema(X_train, preprocessor, feature_metadata)

    model_dir = config.get("output", {}).get("model_dir", "RandomForest/models")
    output_dir = config.get("output", {}).get("output_dir", "RandomForest/outputs")

    save_all_artifacts(
        model=best_rf,
        preprocessor=preprocessor,
        calibrated_model=calibrated_model,
        schema=schema,
        feature_metadata=feature_metadata,
        best_params=best_params,
        train_metrics=train_metrics,
        val_metrics=val_metrics,
        cal_metrics=cal_metrics,
        threshold_info=threshold_result,
        config=config,
        model_dir=model_dir,
        output_dir=output_dir,
    )

    logger.info("=" * 60)
    logger.info(f"EXPERIMENT COMPLETE: {config.get('experiment_name', 'rf_v2')}")
    logger.info(f"Best threshold: {optimal_threshold:.4f}")
    logger.info(f"Test F1 (optimal): {test_metrics_optimal.get('test_optimal_f1', 0):.4f}")
    logger.info(f"Test ROC-AUC: {test_metrics_optimal.get('test_optimal_roc_auc', 0):.4f}")
    logger.info("=" * 60)

    return {
        "model": best_rf,
        "calibrated_model": calibrated_model,
        "preprocessor": preprocessor,
        "threshold": optimal_threshold,
        "metrics": all_metrics,
    }


if __name__ == "__main__":
    main()
