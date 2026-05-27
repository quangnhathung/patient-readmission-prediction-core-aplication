import { HealthApi } from '../api/healthApi.js';
import { HealthResponseDto } from '../dto/HealthResponseDto.js';

export class HealthService {
  constructor() {
    this.api = new HealthApi();
    this.lastCheck = null;
  }

  async check() {
    try {
      const response = await this.api.check();
      const dto = new HealthResponseDto(response.data);
      dto.latency = response.latency;
      this.lastCheck = dto;
      return this.lastCheck;
    } catch (error) {
      this.lastCheck = {
        status: 'offline',
        version: null,
        models_loaded: 0,
        models: [],
        uptime_seconds: 0,
        latency: error.latency || 0,
        error: error.message,
        isHealthy: false,
        formattedUptime: '0s',
      };
      return this.lastCheck;
    }
  }

  getLastCheck() {
    return this.lastCheck;
  }
}
