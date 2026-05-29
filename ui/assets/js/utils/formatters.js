import { RISK_LEVELS } from './constants.js';

export class Formatters {
  static probability(value) {
    return `${(value * 100).toFixed(1)}%`;
  }

  static riskLevel(probability, threshold) {
    if (probability >= threshold) {
      return { level: RISK_LEVELS.HIGH, class: 'high' };
    }
    return { level: RISK_LEVELS.LOW, class: 'low' };
  }

  static modelName(name) {
    const map = {
      'random-forest': 'Random Forest',
      'xgboost': 'XGBoost Ensemble',
      'ensemble': 'Stacking Ensemble',
      'random_forest': 'Random Forest',
      'Ensemble (Random Forest + XGBoost)': 'Stacking Ensemble',
      'Random Forest v2': 'Random Forest',
      'XGBoost Ensemble': 'XGBoost Ensemble',
    };
    return map[name] || name;
  }

  static probabilityBarClass(probability) {
    if (probability >= 0.7) return 'high';
    if (probability >= 0.3) return 'medium';
    return 'low';
  }

  static number(value) {
    return Number(value).toLocaleString('en-US');
  }

  static capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, ' ');
  }
}
