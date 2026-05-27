import { Navbar } from './components/navbar.js';
import { Sidebar } from './components/sidebar.js';
import { Router } from './router.js';
import { HealthService } from './services/healthService.js';
import { PAGES } from './utils/constants.js';

class App {
  constructor() {
    this.healthService = new HealthService();
    this.navbar = null;
    this.sidebar = null;
    this.router = null;
  }

  init() {
    this.navbar = new Navbar();
    this.sidebar = new Sidebar((page) => this.router.navigate(page));
    this.router = new Router(this.navbar, this.sidebar);
    this.router.init();
    this.startHealthCheck();
  }

  startHealthCheck() {
    this.checkHealth();
    setInterval(() => this.checkHealth(), 30000);
  }

  async checkHealth() {
    try {
      const health = await this.healthService.check();
      this.navbar.setHealthStatus(health.isHealthy);
    } catch {
      this.navbar.setHealthStatus(false);
    }
  }
}

const app = new App();
document.addEventListener('DOMContentLoaded', () => {
  app.init();
});
