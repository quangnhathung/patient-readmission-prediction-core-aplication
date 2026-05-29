# Random Forest v2 — Patient Readmission Prediction

Optimized Random Forest model for predicting 30-day hospital readmission risk, built with production-grade ML engineering standards.

---

## Architecture

```
RandomForest/
├── configs/          # YAML/JSON training configurations
├── data/             # Dataset files
├── models/           # Trained model artifacts (joblib + JSON)
├── outputs/          # Metrics and evaluation outputs
├── reports/          # Charts, reports, and evaluation results
├── scripts/          # Training CLI scripts
├── notebooks/        # Jupyter notebooks (optional)
├── src/              # Modular Python source code
│   ├── preprocessing/  # Data cleaning, feature engineering, pipeline
│   ├── training/       # RF training, calibration, threshold tuning
│   ├── evaluation/     # Metrics, charts, reports generation
│   ├── inference/      # Prediction service and schema
│   └── utils/          # Config, logging, artifact management
└── README.md
```

---

## Key Improvements vs Old RF

| Aspect | Old RF (v1) | New RF (v2) |
|--------|-------------|-------------|
| Feature Engineering | None (raw features) | ICD-9 grouping, drug tracking, composite risk, derived features (60 total) |
| Categorical Encoding | `pd.get_dummies` (sparse, 162 cols) | `OrdinalEncoder` (compact, 60 cols) |
| Missing Value Handling | Basic fillna | Robust imputation with sklearn Pipeline |
| Hyperparameter Tuning | GridSearchCV | RandomizedSearchCV + StratifiedKFold |
| Calibration | None | CalibratedClassifierCV (Isotonic) |
| Threshold | Hardcoded 0.2 | F1-optimized (0.17) |
| Training Pipeline | None (external notebook) | Reproducible CLI with YAML config |
| Metrics Tracking | None | JSON, CSV, charts, classification report |
| ROC-AUC | 0.4881 (worse than random) | 0.6521 |

---

## Performance

| Metric | Old RF | New RF v2 | XGBoost Ensemble |
|--------|--------|-----------|-----------------|
| Accuracy | 0.114 | 0.832 | N/A |
| Precision | 0.114 | 0.246 | N/A |
| Recall | 1.000 | 0.231 | N/A |
| F1-Score | 0.205 | 0.239 | N/A |
| ROC-AUC | 0.488 | **0.652** | 0.624 |
| PR-AUC | 0.111 | 0.196 | N/A |

> **Note**: XGBoost numbers from `ensemble_meta_v3.json`. Optimal threshold: 0.17 (F1-maximizing).

---

## Training

### Prerequisites

```bash
pip install scikit-learn pandas numpy pyyaml joblib matplotlib
```

### Quick Start

```bash
python RandomForest/scripts/train.py --config RandomForest/configs/rf_v2.yaml
```

### Custom Training

```bash
# Use custom config
python RandomForest/scripts/train.py --config my_config.yaml

# Override config via command line (modify yaml directly)
```

### Configuration

Edit `RandomForest/configs/rf_v2.yaml`:

```yaml
tuning:
  n_iter: 50           # Number of random search iterations
  cv_folds: 5          # Cross-validation folds
  scoring: "f1"        # Optimization metric

imbalance:
  method: "class_weight"  # class_weight, smote, smotenc, random_under, balanced_rf

calibration:
  method: "isotonic"      # isotonic or sigmoid

threshold:
  metric: "f1"            # f1, youden, or recall
```

### Reproducibility

All experiments are reproducible via:
- Fixed random seed (config: `seed: 42`)
- Full config saved with each trained model
- YAML configuration file tracked in version control

---

## Artifacts

After training, the following artifacts are generated:

### Models (`RandomForest/models/`)

| File | Description |
|------|-------------|
| `random_forest_v2.joblib` | Trained RandomForestClassifier |
| `calibrated_rf_v2.joblib` | CalibratedClassifierCV (isotonic) |
| `preprocessor_v2.joblib` | sklearn ColumnTransformer pipeline |
| `model_schema_v2.json` | Feature names, dtypes, encoding info |
| `feature_metadata_v2.json` | Category mappings per column |
| `best_params_v2.json` | Best hyperparameters from search |
| `training_config_v2.json` | Full training configuration |

### Metrics (`RandomForest/outputs/`)

| File | Description |
|------|-------------|
| `metrics_v2.json` | All metrics (train, val, test, calibration) |

### Reports (`RandomForest/reports/`)

| File | Description |
|------|-------------|
| `confusion_matrix.png` | Confusion matrix on test set |
| `roc_curve.png` | ROC-AUC curve |
| `pr_curve.png` | Precision-Recall curve |
| `feature_importance.png` | Top 30 feature importances |
| `calibration_curve.png` | Calibration before/after |
| `threshold_analysis.png` | Precision/Recall/F1 vs threshold |
| `classification_report.txt` | sklearn classification report |
| `metrics.json` | All metrics in JSON |
| `metrics.csv` | All metrics in CSV |

---

## FastAPI Integration

The new RF v2 model is automatically loaded by the FastAPI backend:

```
POST /api/v1/predict/random-forest?threshold=0.17
```

### How it works:

1. `app/models/registry.py` detects `RandomForest/models/random_forest_v2.joblib` exists
2. Loads the calibrated model + preprocessing pipeline
3. `app/services/prediction.py` calls preprocessor.preprocess() then predict_proba()
4. Default threshold changed from 0.2 to 0.17

### Environment Variables

```env
RANDOM_FOREST_V2_MODEL_PATH=RandomForest/models/random_forest_v2.joblib
RANDOM_FOREST_V2_CALIBRATED_PATH=RandomForest/models/calibrated_rf_v2.joblib
RANDOM_FOREST_V2_PREPROCESSOR_PATH=RandomForest/models/preprocessor_v2.joblib
RANDOM_FOREST_V2_SCHEMA_PATH=RandomForest/models/model_schema_v2.json
```

---

## Inference Example

```python
import joblib
import pandas as pd
from src.preprocessing.feature_engineering import build_features

model = joblib.load("RandomForest/models/calibrated_rf_v2.joblib")
pipeline = joblib.load("RandomForest/models/preprocessor_v2.joblib")

patient = pd.DataFrame([{
    "race": "Caucasian", "gender": "Male", "age": "[70-80)",
    "admission_type_id": 1, "discharge_disposition_id": 1,
    "admission_source_id": 7, "time_in_hospital": 5,
    # ... all 48 fields
}])

features = build_features(patient)
X = pipeline.transform(features)
proba = model.predict_proba(X)[:, 1][0]
prediction = int(proba >= 0.17)
```

---

## Future Improvements

1. **More hyperparameter iterations** (increase `n_iter` for better params)
2. **SMOTE/SMOTENC experiments** (compare with class_weight)
3. **Feature selection** (enable in config + try mutual info)
4. **Deeper calibration comparison** (sigmoid vs isotonic)
5. **Ensemble with XGBoost** (weighted average)
6. **Cross-validation with more folds** (increase `cv_folds`)
7. **Experiment tracking** (MLflow or Weights & Biases integration)
8. **Learning curves** (detect overfitting more precisely)
9. **SHAP analysis** (model interpretability)
10. **Automated retraining pipeline** (CI/CD integration)
