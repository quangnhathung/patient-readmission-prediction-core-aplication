#!/bin/bash
# ============================================================
#  Example cURL commands for Hospital Readmission Prediction API
# ============================================================

BASE_URL="http://localhost:8000/api/v1"

# --- Health check ---
echo "=== Health Check ==="
curl -s "$BASE_URL/health" | jq .

# --- Version ---
echo "=== Version ==="
curl -s "$BASE_URL/version" | jq .

# --- List models ---
echo "=== Models ==="
curl -s "$BASE_URL/models" | jq .

# --- Predict: Logistic Regression ---
echo "=== Predict: Logistic Regression ==="
curl -s -X POST "$BASE_URL/predict/logistic" \
  -H "Content-Type: application/json" \
  -d @examples/predict_payload.json | jq .

# --- Predict: Random Forest ---
echo "=== Predict: Random Forest ==="
curl -s -X POST "$BASE_URL/predict/random-forest" \
  -H "Content-Type: application/json" \
  -d @examples/predict_payload.json | jq .

# --- Predict: XGBoost ---
echo "=== Predict: XGBoost ==="
curl -s -X POST "$BASE_URL/predict/xgboost" \
  -H "Content-Type: application/json" \
  -d @examples/predict_payload.json | jq .

# --- Predict: Ensemble ---
echo "=== Predict: Ensemble ==="
curl -s -X POST "$BASE_URL/predict/ensemble" \
  -H "Content-Type: application/json" \
  -d @examples/predict_payload.json | jq .

# --- Predict: Batch ---
echo "=== Predict: Batch ==="
curl -s -X POST "$BASE_URL/predict/batch?model=xgboost" \
  -H "Content-Type: application/json" \
  -d @examples/batch_payload.json | jq .
