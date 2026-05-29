import { HttpClient } from './httpClient.js';
import { API_PATHS } from '../utils/constants.js';

export class PredictionApi {
  constructor() {
    this.client = new HttpClient();
  }

  async predictRandomForest(data, threshold) {
    let endpoint = API_PATHS.PREDICT_RANDOM_FOREST;
    if (threshold !== null && threshold !== undefined) {
      endpoint += `?threshold=${threshold}`;
    }
    return this.client.post(endpoint, data);
  }

  async predictXGBoost(data, threshold) {
    let endpoint = API_PATHS.PREDICT_XGBOOST;
    if (threshold !== null && threshold !== undefined) {
      endpoint += `?threshold=${threshold}`;
    }
    return this.client.post(endpoint, data);
  }

  async predictEnsemble(data) {
    return this.client.post(API_PATHS.PREDICT_ENSEMBLE, data);
  }

  async predict(model, data, threshold) {
    const modelMap = {
      'random-forest': (d, t) => this.predictRandomForest(d, t),
      'xgboost': (d, t) => this.predictXGBoost(d, t),
      'ensemble': (d) => this.predictEnsemble(d),
    };

    const predictFn = modelMap[model];
    if (!predictFn) {
      throw new Error(`Unknown model: ${model}`);
    }

    return predictFn(data, threshold);
  }
}
