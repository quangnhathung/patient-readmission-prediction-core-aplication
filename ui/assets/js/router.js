import { PAGES } from './utils/constants.js';
import { DashboardView } from './views/dashboardView.js';
import { PredictionView } from './views/predictionView.js';
import { HealthView } from './views/healthView.js';
import { $ } from './utils/helpers.js';

export class Router {
  constructor(navbar, sidebar) {
    this.navbar = navbar;
    this.sidebar = sidebar;
    this.currentPage = null;
    this.views = {};
    this.pageTitles = {
      [PAGES.DASHBOARD]: 'Tổng quan',
      [PAGES.PREDICTION]: 'Dự đoán',
      [PAGES.HEALTH]: 'Sức khỏe hệ thống',
    };
  }

  init() {
    this.registerView(PAGES.DASHBOARD, DashboardView);
    this.registerView(PAGES.PREDICTION, PredictionView);
    this.registerView(PAGES.HEALTH, HealthView);

    document.addEventListener('navigate', (e) => {
      if (e.detail && e.detail.page) {
        this.navigate(e.detail.page);
      }
    });

    this.navigate(PAGES.DASHBOARD);
  }

  registerView(name, ViewClass) {
    this.views[name] = ViewClass;
  }

  navigate(page) {
    if (this.currentPage === page) return;
    if (!this.views[page]) {
      page = PAGES.DASHBOARD;
    }

    this.currentPage = page;
    this.sidebar.setActive(page);
    this.navbar.setTitle(this.pageTitles[page] || page);

    const pageContainer = $('#pageContent');
    if (!pageContainer) return;

    const pages = pageContainer.querySelectorAll('.page');
    pages.forEach((p) => p.classList.remove('active'));

    let pageEl = pageContainer.querySelector(`#page-${page}`);
    if (!pageEl) {
      pageEl = document.createElement('div');
      pageEl.id = `page-${page}`;
      pageEl.className = 'page';
      pageContainer.appendChild(pageEl);
    }

    const ViewClass = this.views[page];
    const viewInstance = new ViewClass(pageEl);
    viewInstance.render();

    pageEl.classList.add('active');
  }
}
