export class Loading {
  constructor() {
    this.overlay = document.getElementById('loadingOverlay');
    if (!this.overlay) {
      this.overlay = document.createElement('div');
      this.overlay.id = 'loadingOverlay';
      this.overlay.className = 'loading-overlay';
      this.overlay.innerHTML = `
        <div class="loading-spinner">
          <div class="spinner"></div>
          <div class="loading-text">Đang xử lý...</div>
        </div>
      `;
      document.body.appendChild(this.overlay);
    }
  }

  show(text) {
    const textEl = this.overlay.querySelector('.loading-text');
    if (textEl && text) {
      textEl.textContent = text;
    }
    this.overlay.classList.add('active');
  }

  hide() {
    this.overlay.classList.remove('active');
  }
}
