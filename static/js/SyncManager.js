// static/js/SyncManager.js
class SyncManager {
    constructor() {
        this.online = navigator.onLine;
        this.syncInProgress = false;
        this.syncIndicator = document.getElementById('syncIndicator');

        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());

        // Initialize DB
        localDB.open().then(() => {
            console.log('IndexedDB ready');
            this.updateIndicator();
        });
    }

    updateIndicator() {
        if (!this.syncIndicator) return;
        if (!this.online) {
            this.syncIndicator.innerHTML = '<span class="badge bg-warning text-dark"><i class="bi bi-cloud-slash"></i> Offline</span>';
        } else if (this.syncInProgress) {
            this.syncIndicator.innerHTML = '<span class="badge bg-info"><i class="bi bi-arrow-repeat"></i> Syncing...</span>';
        } else {
            this.syncIndicator.innerHTML = '<span class="badge bg-success"><i class="bi bi-cloud-check"></i> Online</span>';
        }
    }

    handleOnline() {
        this.online = true;
        this.updateIndicator();
        this.syncQueue();
    }

    handleOffline() {
        this.online = false;
        this.updateIndicator();
    }

    // Cache fresh data from server (called when list pages load)
    async cachePeople() {
        if (!this.online) return;
        try {
            const people = await apiRequest('/api/people');
            await localDB.clear('people');
            for (const p of people) {
                await localDB.put('people', { ...p, _synced: true });
            }
        } catch (e) {
            console.error('Failed to cache people', e);
        }
    }

    async cacheTransactions() {
        if (!this.online) return;
        try {
            const transactions = await apiRequest('/api/transactions');
            await localDB.clear('transactions');
            for (const t of transactions) {
                await localDB.put('transactions', { ...t, _synced: true });
            }
        } catch (e) {
            console.error('Failed to cache transactions', e);
        }
    }

    // Queue an offline action
    async queueAction(action) {
        await localDB.add('syncQueue', {
            ...action,
            timestamp: Date.now()
        });
        this.updatePendingCount();
    }

    async updatePendingCount() {
        const queue = await localDB.getAll('syncQueue');
        if (this.syncIndicator) {
            const badge = this.syncIndicator.querySelector('.badge');
            if (queue.length > 0 && this.online) {
                this.syncIndicator.innerHTML = `<span class="badge bg-info"><i class="bi bi-arrow-repeat"></i> Pending: ${queue.length}</span>`;
            } else if (queue.length > 0 && !this.online) {
                this.syncIndicator.innerHTML = `<span class="badge bg-warning text-dark"><i class="bi bi-cloud-slash"></i> Offline (${queue.length})</span>`;
            } else {
                this.updateIndicator();
            }
        }
    }

    async syncQueue() {
        if (this.syncInProgress || !this.online) return;
        this.syncInProgress = true;
        this.updateIndicator();
        const queue = await localDB.getAll('syncQueue');
        if (queue.length === 0) {
            this.syncInProgress = false;
            this.updateIndicator();
            return;
        }

        // Process in order
        for (const item of queue) {
            try {
                await apiRequest(item.url, {
                    method: item.method,
                    data: item.data,
                    type: 'json'
                });
                // Remove from queue
                await localDB.delete('syncQueue', item.id);
            } catch (e) {
                console.error('Sync failed for', item, e);
                break; // stop on first failure, will retry next time
            }
        }
        // Refresh cache after sync
        await this.cachePeople();
        await this.cacheTransactions();
        this.syncInProgress = false;
        this.updateIndicator();
    }

    // Helper to handle form submissions when offline
    async submitForm(formData, endpoint, method) {
        if (this.online) {
            // Submit to server normally
            const result = await apiRequest(endpoint, { method, data: formData, type: 'json' });
            // Update local cache with result if needed
            return result;
        } else {
            // Save locally and queue
            const tempId = Date.now(); // generate temporary id
            const localItem = { ...formData, id: tempId, _synced: false };
            if (endpoint.includes('people')) {
                await localDB.put('people', localItem);
            } else if (endpoint.includes('transactions')) {
                await localDB.put('transactions', localItem);
            }
            await this.queueAction({ url: endpoint, method, data: formData });
            return localItem;
        }
    }
}