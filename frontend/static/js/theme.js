/**
 * Pricevana Theme Manager
 * Supports Light & Dark mode, OS color-scheme synchronization, and persistence.
 */

(function () {
    const STORAGE_KEY = 'pricevana-theme';

    function getPreferredTheme() {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved === 'dark' || saved === 'light') {
                return saved;
            }
        } catch (e) {
            console.warn('localStorage is not accessible:', e);
        }

        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    function applyTheme(theme) {
        const root = document.documentElement;
        const body = document.body;

        root.setAttribute('data-theme', theme);
        
        // Backward compatibility with legacy theme classes
        if (body) {
            body.classList.remove('theme-light', 'theme-dark', 'theme-lavender', 'theme-midnight', 'theme-cyberpunk');
            body.classList.add(`theme-${theme}`);
        }

        // Update meta color-scheme
        const metaColorScheme = document.querySelector('meta[name="color-scheme"]');
        if (metaColorScheme) {
            metaColorScheme.content = theme;
        }

        // Update Toggle Buttons in the DOM
        const toggleButtons = document.querySelectorAll('.theme-toggle-btn, .theme-circle-btn');
        toggleButtons.forEach(btn => {
            const label = btn.querySelector('.theme-toggle-label');
            if (label) {
                label.textContent = theme === 'dark' ? 'Dark' : 'Light';
            }
            btn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
            btn.setAttribute('data-theme', theme);
        });

        // Save preference
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) {
            console.warn('Unable to persist theme:', e);
        }

        // Dispatch event for charts and reactive components
        window.dispatchEvent(new CustomEvent('pricevana-theme-changed', { detail: { theme } }));
    }

    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        return next;
    }

    // Initialize as early as possible
    const initialTheme = getPreferredTheme();
    applyTheme(initialTheme);

    // Watch OS system preference changes
    if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', (e) => {
            const hasSaved = localStorage.getItem(STORAGE_KEY);
            if (!hasSaved) {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    // Attach to DOM once ready
    document.addEventListener('DOMContentLoaded', () => {
        applyTheme(getPreferredTheme());

        document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                toggleTheme();
            });
        });
    });

    // Expose public API
    window.PricevanaTheme = {
        getTheme: () => document.documentElement.getAttribute('data-theme') || getPreferredTheme(),
        setTheme: applyTheme,
        toggleTheme: toggleTheme
    };
})();
