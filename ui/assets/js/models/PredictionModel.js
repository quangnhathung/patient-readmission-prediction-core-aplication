import { PredictionRequestDto } from '../dto/PredictionRequestDto.js';
import { PredictionResponseDto } from '../dto/PredictionResponseDto.js';

export class PredictionModel {
  constructor() {
    this.selectedModel = null;
    this.threshold = null;
    this.lastPrediction = null;
    this.isLoading = false;
    this.error = null;
  }

  setModel(model) {
    this.selectedModel = model;
  }

  setThreshold(threshold) {
    this.threshold = threshold !== null && threshold !== undefined && threshold !== ''
      ? Number(threshold)
      : null;
  }

  buildRequest(formData) {
    const dto = new PredictionRequestDto(formData);
    return dto.toJSON();
  }

  buildResponse(data) {
    this.lastPrediction = new PredictionResponseDto(data);
    return this.lastPrediction;
  }

  setLoading(loading) {
    this.isLoading = loading;
  }

  setError(error) {
    this.error = error;
  }

  clear() {
    this.lastPrediction = null;
    this.error = null;
    this.isLoading = false;
  }
}
