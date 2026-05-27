export class HealthResponseDto {
  constructor(data) {
    this.status = data.status;
    this.version = data.version;
    this.models_loaded = data.models_loaded;
    this.models = data.models || [];
    this.uptime_seconds = data.uptime_seconds;
  }

  get isHealthy() {
    return this.status === 'healthy';
  }

  get formattedUptime() {
    const hours = Math.floor(this.uptime_seconds / 3600);
    const minutes = Math.floor((this.uptime_seconds % 3600) / 60);
    const seconds = Math.floor(this.uptime_seconds % 60);
    const parts = [];
    if (hours > 0) parts.push(`${hours}h`);
    if (minutes > 0) parts.push(`${minutes}m`);
    parts.push(`${seconds}s`);
    return parts.join(' ');
  }
}
