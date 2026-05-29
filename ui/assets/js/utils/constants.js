export const MODELS = {
  RANDOM_FOREST: 'random-forest',
  XGBOOST: 'xgboost',
  ENSEMBLE: 'ensemble',
};

export const MODEL_LABELS = {
  [MODELS.RANDOM_FOREST]: 'Random Forest',
  [MODELS.XGBOOST]: 'XGBoost Ensemble',
  [MODELS.ENSEMBLE]: 'Stacking Ensemble',
};

export const MODEL_ICONS = {
  [MODELS.RANDOM_FOREST]: '\uD83C\uDF33',
  [MODELS.XGBOOST]: '\u26A1',
  [MODELS.ENSEMBLE]: '\uD83D\uDD17',
};

export const MODEL_DESCRIPTIONS = {
  [MODELS.RANDOM_FOREST]: 'Random Forest v2 với feature engineering, RandomizedSearchCV tuning, và hiệu chuẩn isotonic. Ngưỡng mặc định: 0.17 (tối ưu F1).',
  [MODELS.XGBOOST]: 'Kết hợp XGBoost + LightGBM với hiệu chuẩn isotonic. Sử dụng ngưỡng tối ưu F2 (~0.094).',
  [MODELS.ENSEMBLE]: 'Kết hợp trung bình xác suất từ Random Forest và XGBoost. Tận dụng ưu điểm của cả hai mô hình để dự đoán ổn định hơn. Ngưỡng mặc định: 0.2.',
};

export const RISK_LEVELS = {
  HIGH: 'NGUY CƠ CAO',
  LOW: 'NGUY CƠ THẤP',
};

export const RACE_OPTIONS = [
  { value: 'Caucasian', label: 'Caucasian' },
  { value: 'AfricanAmerican', label: 'African American' },
  { value: 'Hispanic', label: 'Hispanic' },
  { value: 'Asian', label: 'Asian' },
  { value: 'Other', label: 'Other' },
];

export const GENDER_OPTIONS = [
  { value: 'Male', label: 'Nam' },
  { value: 'Female', label: 'Nữ' },
];

export const AGE_RANGES = [
  '[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)',
  '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)',
];

export const ADMISSION_TYPE_IDS = [
  { value: 1, label: 'Cấp cứu' },
  { value: 2, label: 'Khẩn cấp' },
  { value: 3, label: 'Chủ động' },
  { value: 4, label: 'Sơ sinh' },
  { value: 5, label: 'Trung tâm chấn thương' },
  { value: 6, label: 'Không có thông tin' },
  { value: 7, label: 'NULL' },
  { value: 8, label: 'Khác' },
];

export const DISCHARGE_DISPOSITION_IDS = [
  { value: 1, label: 'Về nhà' },
  { value: 2, label: 'Chuyển đến cơ sở khác' },
  { value: 3, label: 'Chuyển đến viện dưỡng lão' },
  { value: 4, label: 'Chuyển đến cơ sở phục hồi chức năng' },
  { value: 5, label: 'Tự ý xuất viện' },
  { value: 6, label: 'Về với dịch vụ y tế tại nhà' },
  { value: 7, label: 'Tử vong' },
  { value: 8, label: 'Chuyển đến cơ sở tâm thần' },
  { value: 9, label: 'Chăm sóc giảm nhẹ' },
  { value: 10, label: 'Chuyển đến cơ sở liên bang' },
  { value: 11, label: 'Chuyển đến tòa án/cơ quan pháp luật' },
  { value: 12, label: 'Không có thông tin' },
  { value: 13, label: 'Khác' },
  { value: 14, label: 'Chuyển đến nhà hỗ trợ sinh hoạt' },
  { value: 15, label: 'Chuyển đến ICU' },
  { value: 16, label: 'Chuyển đến CCU' },
  { value: 17, label: 'Chuyển đến đơn vị chuyển tiếp' },
  { value: 18, label: 'NULL' },
  { value: 19, label: 'Chuyển đến ghép tạng' },
  { value: 20, label: 'Chuyển đến hospice - tại nhà' },
  { value: 21, label: 'Chuyển đến hospice - tại cơ sở' },
  { value: 22, label: 'Chuyển đến chăm sóc dài hạn' },
  { value: 23, label: 'Chuyển đến Medicare/Medicaid' },
  { value: 24, label: 'Chuyển đến bệnh viện khác' },
  { value: 25, label: 'Chuyển đến phục hồi chức năng ngoại trú' },
  { value: 26, label: 'Chuyển đến sức khỏe hành vi' },
  { value: 27, label: 'Chuyển đến điều trị nghiện chất' },
  { value: 28, label: 'Chuyển đến nhà tập thể' },
  { value: 29, label: 'Chuyển đến nơi tạm trú' },
  { value: 30, label: 'Chuyển đến nơi khác' },
];

export const ADMISSION_SOURCE_IDS = [
  { value: 1, label: 'Giới thiệu từ bác sĩ' },
  { value: 2, label: 'Giới thiệu từ phòng khám' },
  { value: 3, label: 'Giới thiệu từ HMO' },
  { value: 4, label: 'Chuyển từ bệnh viện khác' },
  { value: 5, label: 'Chuyển từ viện dưỡng lão' },
  { value: 6, label: 'Chuyển từ cơ sở y tế khác' },
  { value: 7, label: 'Phòng cấp cứu' },
  { value: 8, label: 'Tòa án/Cơ quan pháp luật' },
  { value: 9, label: 'Không có thông tin' },
  { value: 10, label: 'Chuyển từ bệnh viện tiếp cận quan trọng' },
  { value: 11, label: 'Chuyển từ phòng cấp cứu khác' },
  { value: 12, label: 'Chuyển từ hospice' },
  { value: 13, label: 'Chuyển từ phẫu thuật ngoại trú' },
  { value: 14, label: 'Chuyển từ ngoại trú' },
  { value: 15, label: 'Chuyển từ phục hồi chức năng' },
  { value: 16, label: 'Chuyển từ tâm thần' },
  { value: 17, label: 'NULL' },
  { value: 18, label: 'Chuyển từ nơi khác' },
  { value: 19, label: 'Chuyển từ chăm sóc sức khỏe tại nhà' },
  { value: 20, label: 'Chuyển từ nhà hỗ trợ sinh hoạt' },
  { value: 21, label: 'Chuyển từ ICF/MR' },
  { value: 22, label: 'Chuyển từ viện dưỡng lão' },
  { value: 23, label: 'Chuyển từ nội trú bệnh viện khác' },
  { value: 24, label: 'Chuyển từ LTAC' },
  { value: 25, label: 'Chuyển từ phục hồi chức năng nội trú' },
  { value: 26, label: 'Chuyển từ tâm thần nội trú' },
];

export const DRUG_LEVELS = [
  { value: 'No', label: 'Không' },
  { value: 'Down', label: 'Giảm' },
  { value: 'Steady', label: 'Ổn định' },
  { value: 'Up', label: 'Tăng' },
];

export const CHANGE_OPTIONS = [
  { value: 'No', label: 'Không' },
  { value: 'Ch', label: 'Có thay đổi' },
];

export const DIABETES_MED_OPTIONS = [
  { value: 'No', label: 'Không' },
  { value: 'Yes', label: 'Có' },
];

export const MAX_GLU_SERUM_OPTIONS = [
  { value: 'None', label: 'Không có' },
  { value: 'Norm', label: 'Bình thường' },
  { value: '>200', label: '> 200 mg/dL' },
  { value: '>300', label: '> 300 mg/dL' },
];

export const A1C_RESULT_OPTIONS = [
  { value: 'None', label: 'Không có' },
  { value: 'Norm', label: 'Bình thường' },
  { value: '>7', label: '> 7%' },
  { value: '>8', label: '> 8%' },
];

export const THRESHOLD_PRESETS = [0.1, 0.15, 0.2, 0.3, 0.5];

export const API_PATHS = {
  PREDICT_RANDOM_FOREST: '/api/v1/predict/random-forest',
  PREDICT_XGBOOST: '/api/v1/predict/xgboost',
  PREDICT_ENSEMBLE: '/api/v1/predict/ensemble',
  HEALTH: '/api/v1/health',
  DOCS: '/docs',
};

export const PAGES = {
  DASHBOARD: 'dashboard',
  PREDICTION: 'prediction',
  HEALTH: 'health',
};
