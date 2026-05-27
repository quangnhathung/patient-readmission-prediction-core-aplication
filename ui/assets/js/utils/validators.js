export class Validators {
  static required(value, fieldName) {
    if (value === undefined || value === null || value === '') {
      return `${fieldName} là bắt buộc`;
    }
    return null;
  }

  static numeric(value, fieldName) {
    if (value === undefined || value === null || value === '') return null;
    const num = Number(value);
    if (isNaN(num)) {
      return `${fieldName} phải là số hợp lệ`;
    }
    return null;
  }

  static integer(value, fieldName) {
    if (value === undefined || value === null || value === '') return null;
    const num = Number(value);
    if (isNaN(num) || !Number.isInteger(num)) {
      return `${fieldName} phải là số nguyên`;
    }
    return null;
  }

  static range(value, min, max, fieldName) {
    if (value === undefined || value === null || value === '') return null;
    const num = Number(value);
    if (isNaN(num)) return null;
    if (num < min || num > max) {
      return `${fieldName} phải từ ${min} đến ${max}`;
    }
    return null;
  }

  static min(value, min, fieldName) {
    if (value === undefined || value === null || value === '') return null;
    const num = Number(value);
    if (isNaN(num)) return null;
    if (num < min) {
      return `${fieldName} phải ít nhất là ${min}`;
    }
    return null;
  }

  static ageRange(value, fieldName) {
    if (!value) {
      return `${fieldName} là bắt buộc`;
    }
    const validRanges = [
      '[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)',
      '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)',
    ];
    if (!validRanges.includes(value)) {
      return `${fieldName} không hợp lệ`;
    }
    return null;
  }

  static threshold(value, fieldName) {
    if (value === undefined || value === null || value === '') return null;
    const num = Number(value);
    if (isNaN(num) || num < 0 || num > 1) {
      return `${fieldName} phải từ 0 đến 1`;
    }
    return null;
  }

  static validateForm(formData, rules) {
    const errors = {};
    for (const [field, validators] of Object.entries(rules)) {
      for (const validator of validators) {
        const error = validator(formData[field]);
        if (error) {
          errors[field] = error;
          break;
        }
      }
    }
    return errors;
  }
}
