import { PredictionApi } from '../api/predictionApi.js';
import { PredictionModel } from '../models/PredictionModel.js';
import { PredictionRequestDto } from '../dto/PredictionRequestDto.js';

export class PredictionService {
  constructor() {
    this.api = new PredictionApi();
    this.model = new PredictionModel();
  }

  async predict(modelName, formData, threshold) {
    this.model.setLoading(true);
    this.model.setError(null);
    this.model.setModel(modelName);
    this.model.setThreshold(threshold);

    try {
      const dto = new PredictionRequestDto(formData);
      const requestData = dto.toJSON();
      const response = await this.api.predict(modelName, requestData, threshold);
      const predictionDto = this.model.buildResponse(response.data);
      return {
        prediction: predictionDto,
        latency: response.latency,
      };
    } catch (error) {
      this.model.setError(error.message || 'Prediction failed');
      throw error;
    } finally {
      this.model.setLoading(false);
    }
  }

  getLastPrediction() {
    return this.model.lastPrediction;
  }

  isLoading() {
    return this.model.isLoading;
  }

  getError() {
    return this.model.error;
  }

  clear() {
    this.model.clear();
  }
}
