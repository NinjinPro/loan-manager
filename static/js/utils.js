// static/js/utils.js

async function apiRequest(url, options = {}) {
    const {
        method = 'GET',
        data = null,
        headers = {},
        type = 'json'
    } = options;

    const fetchOptions = {
        method,
        headers: { ...headers },
    };

    // Add CSRF token for non‑GET requests
    if (method !== 'GET') {
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) {
            fetchOptions.headers['X-CSRFToken'] = csrfMeta.getAttribute('content');
        }
    }

    if (data) {
        if (type === 'json') {
            fetchOptions.headers['Content-Type'] = 'application/json';
            fetchOptions.body = JSON.stringify(data);
        } else if (type === 'form') {
            fetchOptions.body = new URLSearchParams(data);
        }
    }

    const response = await fetch(url, fetchOptions);
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
    }
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
        return response.json();
    }
    return response.text();
}

function formatRwf(amount) {
    if (amount == null) return '';
    return Number(amount).toLocaleString('en-RW', {
        maximumFractionDigits: 0
    }) + ' Rwf';
}

/* ---- Colour conversion helpers (unchanged) ---- */
function hexToRgb(hex) {
    hex = hex.replace('#', '');
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    return { r, g, b };
}

function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if (max === min) {
        h = s = 0;
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
            case g: h = ((b - r) / d + 2) / 6; break;
            case b: h = ((r - g) / d + 4) / 6; break;
        }
    }
    return { h: h * 360, s: s * 100, l: l * 100 };
}

function hslToHex(h, s, l) {
    s /= 100;
    l /= 100;
    const k = n => (n + h / 30) % 12;
    const a = s * Math.min(l, 1 - l);
    const f = n => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
    const toHex = x => {
        const v = Math.round(255 * f(x));
        return v.toString(16).padStart(2, '0');
    };
    return `#${toHex(0)}${toHex(8)}${toHex(4)}`;
}

function handleOfflineForm(form, endpoint, method = 'POST') {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        loading.show();
        const formData = Object.fromEntries(new FormData(form));
        // Remove csrf_token from the data – it will be sent via header
        delete formData.csrf_token;
        try {
            await window.syncManager.submitForm(formData, endpoint, method);
            window.location.href = form.dataset.redirect || '/';
        } catch (err) {
            alert('Error: ' + err.message);
        } finally {
            loading.hide();
        }
    });
}

window.apiRequest = apiRequest;
window.formatRwf = formatRwf;
window.hexToRgb = hexToRgb;
window.rgbToHsl = rgbToHsl;
window.hslToHex = hslToHex;
window.handleOfflineForm = handleOfflineForm;