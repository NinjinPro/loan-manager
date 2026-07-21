document.addEventListener('DOMContentLoaded', () => {
    window.loading = new LoadingIndicator();
    window.notifications = new NotificationManager();
    window.theme = new ThemeManager();
    window.syncManager = new SyncManager();
});