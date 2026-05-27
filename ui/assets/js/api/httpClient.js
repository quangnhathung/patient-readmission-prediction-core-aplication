import { CONFIG } from '../config.js';

export class HttpClient {
  constructor(baseURL) {
    this.baseURL = baseURL || CONFIG.API_BASE_URL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;

    const body = options.body;
    const payload = (body && typeof body === 'object' && !(body instanceof FormData))
      ? JSON.stringify(body)
      : body;

    if (body && typeof body === 'object' && !(body instanceof FormData)) {
      console.log('Prediction payload:', body);
      console.log('Payload type:', typeof body);
    }

    const config = {
      method: options.method || 'GET',
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
      },
      body: payload,
    };

    const startTime = performance.now();

    try {
      const response = await fetch(url, config);
      const latency = performance.now() - startTime;

      if (!response.ok) {
        const errorData = await this.parseError(response);
        throw new HttpClientError(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData,
          latency
        );
      }

      const data = await response.json();
      return { data, latency, status: response.status };
    } catch (error) {
      if (error instanceof HttpClientError) {
        throw error;
      }
      throw new HttpClientError(
        error.message || 'Network error: Unable to connect to the server',
        0,
        null,
        performance.now() - startTime
      );
    }
  }

  async get(endpoint, headers = {}) {
    return this.request(endpoint, { method: 'GET', headers });
  }

  async post(endpoint, body, headers = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body,
      headers,
    });
  }

  async parseError(response) {
    try {
      return await response.json();
    } catch {
      return { detail: response.statusText || 'Unknown error' };
    }
  }
}

export class HttpClientError extends Error {
  constructor(message, status, data, latency) {
    super(message);
    this.name = 'HttpClientError';
    this.status = status;
    this.data = data;
    this.latency = latency;
  }
}
