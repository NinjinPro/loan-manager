class // static/js/NotificationManager.js

class NotificationManager {
    constructor() {
        this.toastContainer = document.getElementById('toastContainer');
        if (!this.toastContainer) {
            console.warn('Toast container not found');
            return;
        }
        this.pollInterval = 30000; // 30 seconds
        this.fetchAndShow();
        setInterval(() => this.fetchAndShow(), this.pollInterval);
    }

    async fetchAndShow() {
        try {
            const unread = await apiRequest('/api/notifications/unread');
            unread.forEach(notif => this.showToast(notif));
        } catch (err) {
            console.error('Notification fetch error:', err);
        }
    }

    showToast(notification) {
        // Map type to Bootstrap bg class
        const typeClass = {
            info: 'bg-info',
            success: 'bg-success',
            warning: 'bg-warning text-dark',
            error: 'bg-danger'
        }[notification.type] || 'bg-info';
        
        const icon = {
    		info:    'bi-info-circle-fill',
    		success: 'bi-check-circle-fill',
    		warning: 'bi-exclamation-triangle-fill',
    		error:   'bi-x-circle-fill'
		}[notification.type] || 'bi-bell-fill';

        const toastHTML = `
            <div class="toast" role="alert" data-id="${notification.id}">
                <div class="toast-header ${typeClass} text-white">
                	<i class="bi ${icon} me-2"></i>
                    <strong class="me-auto">${notification.type.toUpperCase()}</strong>
                    <small>${new Date(notification.created_at).toLocaleString()}</small>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${this.escapeHtml(notification.message)}
                </div>
            </div>`;
        this.toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        const toastEl = this.toastContainer.lastElementChild;
        const bsToast = new bootstrap.Toast(toastEl, { delay: 5000 });
        bsToast.show();

        // Mark as read when dismissed
        toastEl.addEventListener('hidden.bs.toast', () => {
            apiRequest(`/api/notifications/${notification.id}/read`, { method: 'POST' });
            toastEl.remove();
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}