import { HttpClient } from './httpClient.js';
import { API_PATHS } from '../utils/constants.js';

export class HealthApi {
  constructor() {
    this.client = new HttpClient();
  }

  async check() {
    return this.client.get(API_PATHS.HEALTH);
  }
}
