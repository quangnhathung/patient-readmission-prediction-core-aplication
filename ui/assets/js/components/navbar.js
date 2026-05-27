import { CONFIG } from '../config.js';
import { API_PATHS } from '../utils/constants.js';

export class Navbar {
  constructor() {
    this.element = document.getElementById('navbar');
    this.render();
  }

  render() {
    this.element.innerHTML = `
      <div class="navbar-left">
        <button class="navbar-toggle" id="sidebarToggle" aria-label="Chuyển đổi sidebar">
          &#9776;
        </button>
        <span class="navbar-title" id="navbarTitle">Tổng quan</span>
      </div>
      <div class="navbar-right">
        <a href="${CONFIG.API_BASE_URL}${API_PATHS.DOCS}" target="_blank" class="api-btn" title="Mở tài liệu API">
          <svg class="api-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
          </svg>
          Tài liệu API
        </a>
        <span class="navbar-badge" id="healthBadge">
          <span class="health-dot online" id="healthDot"></span>
          Đang kiểm tra...
        </span>
      </div>
    `;

    this.titleEl = this.element.querySelector('#navbarTitle');
    this.badge = this.element.querySelector('#healthBadge');
    this.healthDot = this.element.querySelector('#healthDot');
  }

  setTitle(title) {
    if (this.titleEl) {
      this.titleEl.textContent = title;
    }
  }

  setHealthStatus(healthy) {
    if (!this.badge || !this.healthDot) return;
    if (healthy) {
      this.badge.className = 'navbar-badge';
      this.healthDot.className = 'health-dot online';
      this.badge.innerHTML = '<span class="health-dot online"></span> API Trực tuyến';
    } else {
      this.badge.className = 'navbar-badge offline';
      this.healthDot.className = 'health-dot offline';
      this.badge.innerHTML = '<span class="health-dot offline"></span> API Ngoại tuyến';
    }
  }
}
