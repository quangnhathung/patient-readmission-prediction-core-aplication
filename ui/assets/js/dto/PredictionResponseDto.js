export class PredictionResponseDto {
  constructor(data) {
    this.prediction = data.prediction;
    this.probability = data.probability;
    this.model_name = data.model_name;
    this.model_version = data.model_version;
    this.threshold = data.threshold;
    this.timestamp = data.timestamp;
    this.status = data.status;
    this.processing_time_ms = data.processing_time_ms;
  }

  get isHighRisk() {
    return this.prediction === 1;
  }

  get probabilityPercent() {
    return (this.probability * 100).toFixed(1);
  }

  get formattedTimestamp() {
    const date = new Date(this.timestamp);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  }

  get formattedProcessingTime() {
    if (this.processing_time_ms < 1000) {
      return `${this.processing_time_ms.toFixed(0)} ms`;
    }
    return `${(this.processing_time_ms / 1000).toFixed(2)} s`;
  }
}
