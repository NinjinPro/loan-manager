// static/js/LoadingIndicator.js

class LoadingIndicator {
    constructor() {
        this.overlay = document.getElementById('loading-overlay');
    }

    show() {
        if (this.overlay) this.overlay.classList.remove('d-none');
    }

    hide() {
        if (this.overlay) this.overlay.classList.add('d-none');
    }
}