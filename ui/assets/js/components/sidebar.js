import { PAGES } from '../utils/constants.js';

export class Sidebar {
  constructor(onNavigate) {
    this.element = document.getElementById('sidebar');
    this.onNavigate = onNavigate;
    this.currentPage = PAGES.DASHBOARD;
    this.render();
    this.attachEvents();
  }

  render() {
    this.element.innerHTML = `
      <div class="sidebar-brand">
        <div class="sidebar-brand-icon">&#9878;</div>
        <div>
          <div class="sidebar-brand-text">Tái nhập viện</div>
          <div class="sidebar-brand-sub">Hệ thống dự đoán</div>
        </div>
      </div>
      <nav class="sidebar-nav">
        <div class="sidebar-nav-item active" data-page="${PAGES.DASHBOARD}">
          <span class="sidebar-nav-icon">&#9632;</span>
          <span class="sidebar-nav-label">Tổng quan</span>
        </div>
        <div class="sidebar-nav-item" data-page="${PAGES.PREDICTION}">
          <span class="sidebar-nav-icon">&#9654;</span>
          <span class="sidebar-nav-label">Dự đoán</span>
        </div>
        <div class="sidebar-nav-item" data-page="${PAGES.HEALTH}">
          <span class="sidebar-nav-icon">&#9881;</span>
          <span class="sidebar-nav-label">Sức khỏe hệ thống</span>
        </div>
      </nav>
      <div class="sidebar-footer">
        Dự đoán Tái nhập viện v1.0
      </div>
    `;
  }

  attachEvents() {
    const items = this.element.querySelectorAll('.sidebar-nav-item');
    items.forEach((item) => {
      item.addEventListener('click', () => {
        const page = item.dataset.page;
        this.navigate(page);
      });
    });

    const toggleBtn = document.getElementById('sidebarToggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        this.element.classList.toggle('open');
        const overlay = document.getElementById('sidebarOverlay');
        if (overlay) overlay.classList.toggle('open');
      });
    }

    const overlay = document.getElementById('sidebarOverlay');
    if (overlay) {
      overlay.addEventListener('click', () => {
        this.element.classList.remove('open');
        overlay.classList.remove('open');
      });
    }
  }

  navigate(page) {
    this.currentPage = page;
    const items = this.element.querySelectorAll('.sidebar-nav-item');
    items.forEach((item) => {
      item.classList.toggle('active', item.dataset.page === page);
    });

    const overlay = document.getElementById('sidebarOverlay');
    if (window.innerWidth <= 768) {
      this.element.classList.remove('open');
      if (overlay) overlay.classList.remove('open');
    }

    if (this.onNavigate) {
      this.onNavigate(page);
    }
  }

  setActive(page) {
    this.currentPage = page;
    const items = this.element.querySelectorAll('.sidebar-nav-item');
    items.forEach((item) => {
      item.classList.toggle('active', item.dataset.page === page);
    });
  }
}
