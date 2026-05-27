import { PredictionForm } from '../components/predictionForm.js';
import { PredictionResult } from '../components/predictionResult.js';
import { PredictionService } from '../services/predictionService.js';
import { Toast } from '../components/toast.js';
import { Loading } from '../components/loading.js';
import { $ } from '../utils/helpers.js';

export class PredictionView {
  constructor(container) {
    this.container = container;
    this.service = new PredictionService();
    this.toast = new Toast();
    this.loading = new Loading();
    this.form = null;
    this.result = null;
  }

  render() {
    this.container.innerHTML = `
      <div id="predictionFormContainer"></div>
      <div id="predictionResult"></div>
    `;

    const formContainer = $('#predictionFormContainer', this.container);
    const resultContainer = $('#predictionResult', this.container);

    this.form = new PredictionForm(formContainer, (data) => this.handleSubmit(data));
    this.result = new PredictionResult(resultContainer);
  }

  async handleSubmit(data) {
    this.loading.show('Đang dự đoán...');

    try {
      const formData = this.form.getValues();
      const result = await this.service.predict(data.model, formData, data.threshold);

      this.result.render(result.prediction, result.latency);
      this.toast.success(
        'Dự đoán thành công',
        `${result.prediction.isHighRisk ? 'Nguy cơ cao' : 'Nguy cơ thấp'} tái nhập viện`
      );
    } catch (error) {
      this.result.showError(error.message || 'Đã xảy ra lỗi không mong muốn');
      this.toast.error(
        'Dự đoán thất bại',
        error.message || 'Không thể hoàn thành dự đoán'
      );
    } finally {
      this.loading.hide();
      if (this.form) {
        this.form.enableSubmit();
      }
    }
  }
}
