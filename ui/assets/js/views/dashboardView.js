import { MODELS, MODEL_LABELS, MODEL_ICONS, MODEL_DESCRIPTIONS } from '../utils/constants.js';
import { HealthService } from '../services/healthService.js';

export class DashboardView {
  constructor(container) {
    this.container = container;
    this.healthService = new HealthService();
  }

  render() {
    this.container.innerHTML = `
      <div class="page-title">Tổng quan hệ thống</div>
      <div class="page-subtitle">Tổng quan hệ thống và trạng thái mô hình</div>

      <div class="stat-grid" id="dashboardStats">
        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-label">Trạng thái API</span>
            <div class="stat-card-icon icon-primary">&#9878;</div>
          </div>
          <div class="stat-card-value" id="dashApiStatus">Đang kiểm tra...</div>
          <div class="stat-card-desc" id="dashApiVersion"></div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-label">Mô hình đã tải</span>
            <div class="stat-card-icon icon-success">&#9733;</div>
          </div>
          <div class="stat-card-value" id="dashModelsCount">-</div>
          <div class="stat-card-desc" id="dashModelsList"></div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-label">Thời gian hoạt động</span>
            <div class="stat-card-icon icon-warning">&#9201;</div>
          </div>
          <div class="stat-card-value" id="dashUptime">-</div>
          <div class="stat-card-desc">Thời gian hoạt động</div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-label">Độ trễ</span>
            <div class="stat-card-icon icon-info">&#9881;</div>
          </div>
          <div class="stat-card-value" id="dashLatency">-</div>
          <div class="stat-card-desc">Thời gian phản hồi API</div>
        </div>
      </div>

      <div class="card mb-lg">
        <div class="card-header">
          <div>
            <div class="card-title">Mô hình khả dụng</div>
            <div class="card-subtitle">Chọn mô hình để dự đoán tái nhập viện</div>
          </div>
        </div>
        <div class="card-body">
          <div class="models-grid">
            ${this.renderModelCard(MODELS.RANDOM_FOREST)}
            ${this.renderModelCard(MODELS.XGBOOST)}
            ${this.renderModelCard(MODELS.ENSEMBLE)}
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Bắt đầu nhanh</div>
            <div class="card-subtitle">Bắt đầu với dự đoán tái nhập viện</div>
          </div>
        </div>
        <div class="card-body">
          <div class="stat-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
            <div class="stat-card" style="cursor:pointer;" id="quickPredict">
              <div class="stat-card-header">
                <span class="stat-card-label">Bước 1</span>
                <div class="stat-card-icon icon-primary">&#9654;</div>
              </div>
              <div class="stat-card-value" style="font-size:var(--font-base);">Dự đoán</div>
              <div class="stat-card-desc">Nhập dữ liệu bệnh nhân và chạy dự đoán</div>
            </div>
            <div class="stat-card" style="cursor:pointer;" id="quickHealth">
              <div class="stat-card-header">
                <span class="stat-card-label">Bước 2</span>
                <div class="stat-card-icon icon-info">&#9881;</div>
              </div>
              <div class="stat-card-value" style="font-size:var(--font-base);">Kiểm tra sức khỏe</div>
              <div class="stat-card-desc">Xem trạng thái hệ thống và mô hình</div>
            </div>
            <div class="stat-card">
              <div class="stat-card-header">
                <span class="stat-card-label">Bước 3</span>
                <div class="stat-card-icon icon-success">&#9733;</div>
              </div>
              <div class="stat-card-value" style="font-size:var(--font-base);">Xem kết quả</div>
              <div class="stat-card-desc">Phân tích kết quả dự đoán và rủi ro</div>
            </div>
          </div>
        </div>
      </div>
    `;

    this.refresh();

    const quickPredict = this.container.querySelector('#quickPredict');
    const quickHealth = this.container.querySelector('#quickHealth');

    if (quickPredict) {
      quickPredict.addEventListener('click', () => {
        document.dispatchEvent(new CustomEvent('navigate', { detail: { page: 'prediction' } }));
      });
    }
    if (quickHealth) {
      quickHealth.addEventListener('click', () => {
        document.dispatchEvent(new CustomEvent('navigate', { detail: { page: 'health' } }));
      });
    }
  }

  renderModelCard(model) {
    return `
      <div class="model-card">
        <div class="model-card-header">
          <div class="model-card-icon icon-primary">${MODEL_ICONS[model]}</div>
          <span class="badge badge-success">Khả dụng</span>
        </div>
        <div class="model-card-name">${MODEL_LABELS[model]}</div>
        <div class="model-card-desc">${MODEL_DESCRIPTIONS[model]}</div>
      </div>
    `;
  }

  async refresh() {
    const health = await this.healthService.check();

    const statusEl = this.container.querySelector('#dashApiStatus');
    const versionEl = this.container.querySelector('#dashApiVersion');
    const modelsCountEl = this.container.querySelector('#dashModelsCount');
    const modelsListEl = this.container.querySelector('#dashModelsList');
    const uptimeEl = this.container.querySelector('#dashUptime');
    const latencyEl = this.container.querySelector('#dashLatency');

    if (health.isHealthy) {
      if (statusEl) {
        statusEl.textContent = 'Trực tuyến';
        statusEl.style.color = 'var(--color-success)';
      }
      if (versionEl) versionEl.textContent = `v${health.version}`;
    } else {
      if (statusEl) {
        statusEl.textContent = 'Ngoại tuyến';
        statusEl.style.color = 'var(--color-danger)';
      }
      if (versionEl) versionEl.textContent = 'Không khả dụng';
    }

    if (modelsCountEl) modelsCountEl.textContent = health.models_loaded;
    if (modelsListEl) {
      modelsListEl.textContent = health.models && health.models.length > 0
        ? health.models.join(', ')
        : 'Chưa có mô hình nào';
    }
    if (uptimeEl) uptimeEl.textContent = health.formattedUptime || 'Không có';
    if (latencyEl) latencyEl.textContent = `${health.latency.toFixed(0)} ms`;
  }
}
