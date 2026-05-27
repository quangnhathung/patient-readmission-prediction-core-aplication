import { HealthService } from '../services/healthService.js';
import { MODELS, MODEL_LABELS, MODEL_ICONS } from '../utils/constants.js';

export class HealthView {
  constructor(container) {
    this.container = container;
    this.service = new HealthService();
  }

  render() {
    this.container.innerHTML = `
      <div class="page-title">Sức khỏe hệ thống</div>
      <div class="page-subtitle">Giám sát trạng thái API và mô hình</div>

      <div class="card mb-lg">
        <div class="card-header">
          <div>
            <div class="card-title">Trạng thái API</div>
            <div class="card-subtitle">Giám sát sức khỏe API theo thời gian thực</div>
          </div>
          <button class="btn btn-primary btn-sm" id="refreshHealthBtn">&#8635; Làm mới</button>
        </div>
        <div class="card-body">
          <div class="health-status-grid" id="healthStatusGrid">
            <div class="stat-card">
              <div class="stat-card-header">
                <span class="stat-card-label">Trạng thái</span>
                <div class="stat-card-icon icon-primary">&#9878;</div>
              </div>
              <div class="stat-card-value" id="healthStatusValue">Đang kiểm tra...</div>
              <div class="stat-card-desc" id="healthVersion"></div>
            </div>
            <div class="stat-card">
              <div class="stat-card-header">
                <span class="stat-card-label">Thời gian phản hồi</span>
                <div class="stat-card-icon icon-info">&#9201;</div>
              </div>
              <div class="stat-card-value" id="healthLatency">-</div>
              <div class="stat-card-desc">Độ trễ API</div>
            </div>
            <div class="stat-card">
              <div class="stat-card-header">
                <span class="stat-card-label">Mô hình đã tải</span>
                <div class="stat-card-icon icon-success">&#9733;</div>
              </div>
              <div class="stat-card-value" id="healthModelsCount">-</div>
              <div class="stat-card-desc" id="healthModelsList"></div>
            </div>
            <div class="stat-card">
              <div class="stat-card-header">
                <span class="stat-card-label">Thời gian hoạt động</span>
                <div class="stat-card-icon icon-warning">&#9881;</div>
              </div>
              <div class="stat-card-value" id="healthUptime">-</div>
              <div class="stat-card-desc">Thời gian hoạt động</div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Danh sách mô hình</div>
            <div class="card-subtitle">Các mô hình dự đoán khả dụng</div>
          </div>
        </div>
        <div class="card-body">
          <div class="models-grid">
            ${this.renderModelHealthCard('random-forest')}
            ${this.renderModelHealthCard('xgboost')}
          </div>
        </div>
      </div>
    `;

    this.refresh();

    const refreshBtn = this.container.querySelector('#refreshHealthBtn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.refresh());
    }
  }

  renderModelHealthCard(model) {
    return `
      <div class="model-card">
        <div class="model-card-header">
          <div class="model-card-icon icon-primary">${MODEL_ICONS[model] || '?'}</div>
          <span class="badge badge-success" id="modelBadge_${model}">Khả dụng</span>
        </div>
        <div class="model-card-name">${MODEL_LABELS[model] || model}</div>
        <div class="model-card-desc">
          Sẵn sàng dự đoán. Sử dụng ngưỡng mặc định tối ưu hiệu suất.
        </div>
      </div>
    `;
  }

  async refresh() {
    const health = await this.service.check();

    const statusValue = this.container.querySelector('#healthStatusValue');
    const versionEl = this.container.querySelector('#healthVersion');
    const latencyEl = this.container.querySelector('#healthLatency');
    const modelsCountEl = this.container.querySelector('#healthModelsCount');
    const modelsListEl = this.container.querySelector('#healthModelsList');
    const uptimeEl = this.container.querySelector('#healthUptime');

    if (health.isHealthy) {
      if (statusValue) {
        statusValue.textContent = 'Tốt';
        statusValue.style.color = 'var(--color-success)';
      }
      if (versionEl) versionEl.textContent = `API v${health.version}`;
    } else {
      if (statusValue) {
        statusValue.textContent = 'Không tốt';
        statusValue.style.color = 'var(--color-danger)';
      }
      if (versionEl) versionEl.textContent = health.error || 'Không khả dụng';
    }

    if (latencyEl) latencyEl.textContent = `${health.latency.toFixed(0)} ms`;
    if (modelsCountEl) modelsCountEl.textContent = health.models_loaded;
    if (modelsListEl) {
      modelsListEl.textContent = health.models && health.models.length > 0
        ? health.models.join(', ')
        : 'Chưa có mô hình nào';
    }
    if (uptimeEl) uptimeEl.textContent = health.formattedUptime || 'Không có';
  }
}
