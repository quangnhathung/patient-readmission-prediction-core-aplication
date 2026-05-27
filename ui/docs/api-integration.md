# Tích hợp API

## Base URL

Tất cả request API được gửi đến `http://localhost:8000` (có thể cấu hình trong `assets/js/config.js`).

## Endpoints

### Kiểm tra sức khỏe

```
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": 2,
  "models": ["random-forest", "xgboost"],
  "uptime_seconds": 3600.0
}
```

Được sử dụng cho: Chỉ báo trạng thái Dashboard, huy hiệu sức khỏe navbar, trang Sức khỏe Hệ thống.

### Dự đoán Random Forest

```
POST /api/v1/predict/random-forest?threshold=0.2
```

**Request Body** (schema PatientData):
```json
{
  "race": "Caucasian",
  "gender": "Male",
  "age": "[60-70)",
  "admission_type_id": 1,
  "discharge_disposition_id": 1,
  "admission_source_id": 7,
  "time_in_hospital": 5,
  "payer_code": "MC",
  "medical_specialty": "Cardiology",
  "num_lab_procedures": 41,
  "num_procedures": 2,
  "num_medications": 12,
  "number_outpatient": 0,
  "number_emergency": 0,
  "number_inpatient": 0,
  "number_diagnoses": 6,
  "max_glu_serum": "None",
  "A1Cresult": "None",
  "metformin": "No",
  "repaglinide": "No",
  "insulin": "No",
  "change": "No",
  "diabetesMed": "No",
  "diag_1": "428.0",
  "diag_2": null,
  "diag_3": null
}
```

**Tham số Query:**
- `threshold` (tùy chọn, float 0.0–1.0) — Ngưỡng phân loại tùy chỉnh

**Response:**
```json
{
  "prediction": 1,
  "probability": 0.85,
  "model_name": "random-forest",
  "model_version": "1.0.0",
  "threshold": 0.2,
  "timestamp": "2024-01-01T00:00:00",
  "status": "success",
  "processing_time_ms": 45.2
}
```

### Dự đoán XGBoost Ensemble

```
POST /api/v1/predict/xgboost?threshold=0.5
```

Cùng định dạng request/response như Random Forest, nhưng sử dụng kết hợp XGBoost + LightGBM với hiệu chuẩn isotonic.

## Ngưỡng (Threshold)

Tham số query `threshold` cho phép tùy chỉnh ngưỡng phân loại:

| Threshold | Hành vi |
|-----------|---------|
| Không cung cấp | Sử dụng mặc định của mô hình (0.2 cho RF, F2-optimal cho XGBoost) |
| 0.0–1.0 | Ngưỡng tùy chỉnh; probability >= threshold = nguy cơ cao |

## Response lỗi

```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "detail": "age must match pattern '^\\[\\d+-\\d+\\)$'"
}
```

Mã lỗi phổ biến: `VALIDATION_ERROR`, `MODEL_NOT_FOUND`, `INTERNAL_ERROR`.

## CORS

Backend CORS middleware được cấu hình để cho phép request từ `http://localhost:5500` (cổng Live Server mặc định). Nếu sử dụng cổng khác, cập nhật cấu hình CORS backend hoặc `config.js`.
