import { Formatters } from '../utils/formatters.js';

export class PredictionResult {
  constructor(container) {
    this.container = container;
  }

  render(prediction, latency) {
    const risk = Formatters.riskLevel(prediction.probability, prediction.threshold);
    const barClass = Formatters.probabilityBarClass(prediction.probability);

    this.container.innerHTML = `
      <div class="result-card">
        <div class="result-header">
          <div>
            <div class="card-title">Kết quả dự đoán</div>
            <div class="card-subtitle">${prediction.formattedTimestamp}</div>
          </div>
          <span class="result-risk-badge ${risk.class}">${risk.level}</span>
        </div>

        <div class="result-probability">
          <div class="result-probability-label">
            <span>Xác suất tái nhập viện</span>
            <span class="result-probability-value">${Formatters.probability(prediction.probability)}</span>
          </div>
          <div class="progress-bar">
            <div class="progress-bar-fill ${barClass}" style="width: ${prediction.probabilityPercent}%"></div>
          </div>
        </div>

        <div class="result-details">
          <div class="result-detail-item">
            <div class="result-detail-label">Kết quả</div>
            <div class="result-detail-value">${prediction.isHighRisk ? 'Nguy cơ cao (Tái nhập viện)' : 'Nguy cơ thấp (Không tái nhập)'}</div>
          </div>
          <div class="result-detail-item">
            <div class="result-detail-label">Mô hình</div>
            <div class="result-detail-value">${Formatters.modelName(prediction.model_name)}</div>
          </div>
          <div class="result-detail-item">
            <div class="result-detail-label">Phiên bản</div>
            <div class="result-detail-value">${prediction.model_version}</div>
          </div>
          <div class="result-detail-item">
            <div class="result-detail-label">Ngưỡng</div>
            <div class="result-detail-value">${prediction.threshold}</div>
          </div>
          <div class="result-detail-item">
            <div class="result-detail-label">Thời gian xử lý</div>
            <div class="result-detail-value">${prediction.formattedProcessingTime}</div>
          </div>
          <div class="result-detail-item">
            <div class="result-detail-label">Độ trễ</div>
            <div class="result-detail-value">${latency ? `${latency.toFixed(0)} ms` : 'Không có'}</div>
          </div>
        </div>
      </div>
    `;

    this.container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  showError(message) {
    this.container.innerHTML = `
      <div class="result-card">
        <div class="empty-state">
          <div class="empty-state-icon">&#9888;</div>
          <div class="empty-state-title">Dự đoán thất bại</div>
          <div class="empty-state-text">${message}</div>
        </div>
      </div>
    `;
  }

  clear() {
    this.container.innerHTML = '';
  }
}
