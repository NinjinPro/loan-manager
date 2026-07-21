// static/js/ThemeManager.js

class ThemeManager {
    constructor() {
        this.colorPicker = document.getElementById('mainColorPicker');
        this.previewContainer = document.getElementById('colorPreview') || null;
        if (this.colorPicker) {
            this.colorPicker.addEventListener('input', (e) => this.previewColor(e.target.value));
        }
    }

    /**
     * Generate shades from a hex colour.
     * Returns an object: { "100": "#hex", "95": ..., ... "5": ... }
     */
    generateShades(hex) {
        const { r, g, b } = hexToRgb(hex);
        const { h, s } = rgbToHsl(r, g, b);
        const shades = {};
        for (let i = 0; i < 20; i++) {
            const lightness = 100 - (i * (95 / 19)); // 100% down to 5%
            const percent = 100 - i * 5;
            shades[`${percent}`] = hslToHex(h, s, lightness);
        }
        return shades;
    }

    /**
     * Update CSS custom properties on :root with the new shades.
     */
    previewColor(hex) {
        const shades = this.generateShades(hex);
        for (const [percent, color] of Object.entries(shades)) {
            document.documentElement.style.setProperty(`--theme-${percent}`, color);
        }
        // Update primary button colours if using bootstrap overrides
        document.documentElement.style.setProperty('--bs-primary', shades['80']);
        document.documentElement.style.setProperty('--bs-success', shades['70']);
        // Optionally render a small preview swatch
        if (this.previewContainer) {
            this.previewContainer.innerHTML = '';
            for (const [p, col] of Object.entries(shades)) {
                const swatch = document.createElement('div');
                swatch.style.backgroundColor = col;
                swatch.style.width = '20px';
                swatch.style.height = '20px';
                swatch.style.display = 'inline-block';
                swatch.title = `${p}%`;
                this.previewContainer.appendChild(swatch);
            }
        }
    }
}