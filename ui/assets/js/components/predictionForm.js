import {
  GENDER_OPTIONS, AGE_RANGES, ADMISSION_TYPE_IDS, DISCHARGE_DISPOSITION_IDS,
  ADMISSION_SOURCE_IDS, DRUG_LEVELS, CHANGE_OPTIONS, DIABETES_MED_OPTIONS,
  MAX_GLU_SERUM_OPTIONS, A1C_RESULT_OPTIONS, THRESHOLD_PRESETS, RACE_OPTIONS,
  MODELS, MODEL_LABELS, MODEL_ICONS, MODEL_DESCRIPTIONS,
} from '../utils/constants.js';
import { Validators } from '../utils/validators.js';
import { $ } from '../utils/helpers.js';

export class PredictionForm {
  constructor(container, onSubmit) {
    this.container = container;
    this.onSubmit = onSubmit;
    this.selectedModel = MODELS.RANDOM_FOREST;
    this.threshold = null;
    this.render();
    this.attachEvents();
  }

  render() {
    this.container.innerHTML = `
      <div class="prediction-form-container">
        <div class="page-title">Dự đoán tái nhập viện</div>
        <div class="page-subtitle">Nhập thông tin bệnh nhân để dự đoán nguy cơ tái nhập viện trong 30 ngày</div>

        <div class="model-selector" id="modelSelector">
          ${this.renderModelOption(MODELS.RANDOM_FOREST, true)}
          ${this.renderModelOption(MODELS.XGBOOST, false)}
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Thông tin bệnh nhân</div>
              <div class="card-subtitle">Điền thông tin chi tiết của bệnh nhân bên dưới</div>
            </div>
          </div>
          <div class="card-body">
            <form id="predictionForm" novalidate>
              <div class="form-section">
                <div class="form-section-title">Nhân khẩu học</div>
                <div class="form-row">
                  ${this.renderFormSelect('race', 'Chủng tộc', RACE_OPTIONS, false)}
                  ${this.renderFormSelect('gender', 'Giới tính', GENDER_OPTIONS, true)}
                  ${this.renderFormSelect('age', 'Độ tuổi', AGE_RANGES.map(a => ({ value: a, label: a })), true)}
                </div>
              </div>

              <div class="form-section">
                <div class="form-section-title">Chi tiết nhập viện</div>
                <div class="form-row">
                  ${this.renderFormSelect('admission_type_id', 'Loại nhập viện', ADMISSION_TYPE_IDS, true)}
                  ${this.renderFormSelect('discharge_disposition_id', 'Hình thức xuất viện', DISCHARGE_DISPOSITION_IDS, true)}
                  ${this.renderFormSelect('admission_source_id', 'Nguồn nhập viện', ADMISSION_SOURCE_IDS, true)}
                </div>
                <div class="form-row" style="margin-top: var(--spacing-md)">
                  ${this.renderFormField('number', 'time_in_hospital', 'Số ngày nằm viện', '1 - 30 ngày', true)}
                  ${this.renderFormField('text', 'medical_specialty', 'Chuyên khoa', 'VD: Tim mạch', false)}
                </div>
              </div>

              <div class="form-section">
                <div class="form-section-title">Chỉ số lâm sàng</div>
                <div class="form-row">
                  ${this.renderFormField('number', 'num_lab_procedures', 'Số xét nghiệm', 'Số lượng xét nghiệm', true)}
                  ${this.renderFormField('number', 'num_procedures', 'Số thủ thuật', 'Số lượng thủ thuật', true)}
                  ${this.renderFormField('number', 'num_medications', 'Số thuốc', 'Số lượng thuốc', true)}
                </div>
                <div class="form-row" style="margin-top: var(--spacing-md)">
                  ${this.renderFormField('number', 'number_outpatient', 'Khám ngoại trú', 'Trong năm qua', true)}
                  ${this.renderFormField('number', 'number_emergency', 'Khám cấp cứu', 'Trong năm qua', true)}
                  ${this.renderFormField('number', 'number_inpatient', 'Nhập viện', 'Trong năm qua', true)}
                </div>
                <div class="form-row" style="margin-top: var(--spacing-md)">
                  ${this.renderFormField('number', 'number_diagnoses', 'Số chẩn đoán', 'Tổng số chẩn đoán', true)}
                  ${this.renderFormSelect('max_glu_serum', 'Đường huyết tối đa', MAX_GLU_SERUM_OPTIONS, false)}
                  ${this.renderFormSelect('A1Cresult', 'Kết quả A1C', A1C_RESULT_OPTIONS, false)}
                </div>
              </div>

              <div class="form-section">
                <div class="form-section-title">Thông tin thuốc</div>
                <div class="form-row">
                  ${this.renderFormSelect('metformin', 'Metformin', DRUG_LEVELS, false)}
                  ${this.renderFormSelect('insulin', 'Insulin', DRUG_LEVELS, false)}
                  ${this.renderFormSelect('change', 'Thay đổi thuốc', CHANGE_OPTIONS, false)}
                  ${this.renderFormSelect('diabetesMed', 'Thuốc tiểu đường', DIABETES_MED_OPTIONS, false)}
                </div>
              </div>

              <div class="form-section">
                <div class="form-section-title">Mã chẩn đoán (ICD-9)</div>
                <div class="form-row">
                  ${this.renderFormField('text', 'diag_1', 'Chẩn đoán chính', 'VD: 428.0', false)}
                  ${this.renderFormField('text', 'diag_2', 'Chẩn đoán phụ', 'VD: 250.0', false)}
                  ${this.renderFormField('text', 'diag_3', 'Chẩn đoán thứ ba', 'VD: 401.9', false)}
                </div>
              </div>

              <div class="form-section">
                <div class="form-section-title">Cài đặt ngưỡng</div>
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Ngưỡng phân loại (không bắt buộc)</label>
                    <div class="threshold-input-group">
                      <input type="number" id="thresholdInput" class="form-input" step="0.05" min="0" max="1" placeholder="Mặc định" style="max-width: 160px">
                      <div class="threshold-presets">
                        ${THRESHOLD_PRESETS.map(t => `<button type="button" class="threshold-preset" data-value="${t}">${t}</button>`).join('')}
                      </div>
                    </div>
                    <div class="form-hint">Để trống để sử dụng ngưỡng mặc định của mô hình</div>
                  </div>
                </div>
              </div>

              <div class="prediction-form-actions">
                <button type="submit" class="btn btn-primary btn-lg" id="predictBtn">
                  &#9654; Dự đoán
                </button>
                <button type="button" class="btn btn-secondary btn-lg" id="resetBtn">
                  Làm mới
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    `;
  }

  renderModelOption(model, selected) {
    return `
      <div class="model-option ${selected ? 'selected' : ''}" data-model="${model}">
        <div class="model-option-icon">${MODEL_ICONS[model]}</div>
        <div class="model-option-name">${MODEL_LABELS[model]}</div>
        <div class="model-option-desc">${MODEL_DESCRIPTIONS[model]}</div>
      </div>
    `;
  }

  renderFormField(type, name, label, placeholder, required) {
    return `
      <div class="form-group" data-field="${name}">
        <label class="form-label" for="${name}">${label}${required ? '<span class="required">*</span>' : ''}</label>
        <input type="${type}" id="${name}" name="${name}" class="form-input" placeholder="${placeholder}" ${required ? 'required' : ''}>
        <div class="form-error hidden" data-error="${name}"></div>
      </div>
    `;
  }

  renderFormSelect(name, label, options, required) {
    const opts = options.map(o =>
      `<option value="${o.value}">${o.label}</option>`
    ).join('');
    return `
      <div class="form-group" data-field="${name}">
        <label class="form-label" for="${name}">${label}${required ? '<span class="required">*</span>' : ''}</label>
        <select id="${name}" name="${name}" class="form-select" ${required ? 'required' : ''}>
          <option value="">${required ? '-- Chọn --' : '-- Không --'}</option>
          ${opts}
        </select>
        <div class="form-error hidden" data-error="${name}"></div>
      </div>
    `;
  }

  attachEvents() {
    const form = $('#predictionForm', this.container);
    const modelOptions = this.container.querySelectorAll('.model-option');
    const thresholdInput = $('#thresholdInput', this.container);
    const thresholdPresets = this.container.querySelectorAll('.threshold-preset');
    const predictBtn = $('#predictBtn', this.container);
    const resetBtn = $('#resetBtn', this.container);

    modelOptions.forEach((opt) => {
      opt.addEventListener('click', () => {
        modelOptions.forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');
        this.selectedModel = opt.dataset.model;
      });
    });

    thresholdPresets.forEach((btn) => {
      btn.addEventListener('click', () => {
        thresholdPresets.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        thresholdInput.value = btn.dataset.value;
      });
    });

    thresholdInput.addEventListener('input', () => {
      thresholdPresets.forEach(b => b.classList.remove('active'));
      this.threshold = thresholdInput.value || null;
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (this.validateForm()) {
        predictBtn.disabled = true;
        if (this.onSubmit) {
          this.onSubmit({
            model: this.selectedModel,
            threshold: thresholdInput.value || null,
          });
        }
      }
    });

    resetBtn.addEventListener('click', () => {
      form.reset();
      this.clearErrors();
      thresholdPresets.forEach(b => b.classList.remove('active'));
      const result = document.getElementById('predictionResult');
      if (result) result.innerHTML = '';
    });
  }

  validateForm() {
    const form = $('#predictionForm', this.container);
    const formData = new FormData(form);
    let isValid = true;

    this.clearErrors();

    const rules = {
      gender: [v => Validators.required(v, 'Giới tính')],
      age: [v => Validators.ageRange(v, 'Độ tuổi')],
      admission_type_id: [v => Validators.required(v, 'Loại nhập viện')],
      discharge_disposition_id: [v => Validators.required(v, 'Hình thức xuất viện')],
      admission_source_id: [v => Validators.required(v, 'Nguồn nhập viện')],
      time_in_hospital: [
        v => Validators.required(v, 'Số ngày nằm viện'),
        v => Validators.range(v, 1, 30, 'Số ngày nằm viện'),
      ],
      num_lab_procedures: [v => Validators.min(v, 0, 'Số xét nghiệm')],
      num_procedures: [v => Validators.min(v, 0, 'Số thủ thuật')],
      num_medications: [v => Validators.min(v, 0, 'Số thuốc')],
      number_outpatient: [v => Validators.min(v, 0, 'Khám ngoại trú')],
      number_emergency: [v => Validators.min(v, 0, 'Khám cấp cứu')],
      number_inpatient: [v => Validators.min(v, 0, 'Nhập viện')],
      number_diagnoses: [v => Validators.min(v, 0, 'Số chẩn đoán')],
    };

    for (const [field, validators] of Object.entries(rules)) {
      const value = formData.get(field);
      for (const validator of validators) {
        const error = validator(value);
        if (error) {
          this.showFieldError(field, error);
          isValid = false;
          break;
        }
      }
    }

    const thresholdVal = $('#thresholdInput', this.container).value;
    if (thresholdVal) {
      const thresholdError = Validators.threshold(thresholdVal, 'Ngưỡng phân loại');
      if (thresholdError) {
        this.showFieldError('thresholdInput', thresholdError, true);
        isValid = false;
      }
    }

    return isValid;
  }

  clearErrors() {
    const errors = this.container.querySelectorAll('.form-error');
    errors.forEach(el => {
      el.textContent = '';
      el.classList.add('hidden');
    });
    const inputs = this.container.querySelectorAll('.form-input.error, .form-select.error');
    inputs.forEach(el => el.classList.remove('error'));
  }

  showFieldError(field, message, isInput = false) {
    if (isInput) {
      const input = $(`#${field}`, this.container);
      if (input) input.classList.add('error');
      return;
    }
    const errorEl = this.container.querySelector(`[data-error="${field}"]`);
    const inputEl = this.container.querySelector(`#${field}`);
    if (errorEl) {
      errorEl.textContent = message;
      errorEl.classList.remove('hidden');
    }
    if (inputEl) {
      inputEl.classList.add('error');
    }
  }

  enableSubmit() {
    const btn = $('#predictBtn', this.container);
    if (btn) btn.disabled = false;
  }

  getValues() {
    const form = $('#predictionForm', this.container);
    const data = {};
    const formData = new FormData(form);
    for (const [key, value] of formData.entries()) {
      data[key] = value;
    }
    return data;
  }

  getSelectedModel() {
    return this.selectedModel;
  }

  getThreshold() {
    const input = $('#thresholdInput', this.container);
    return input.value || null;
  }
}
