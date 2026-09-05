/**
 * Pricevana Global Configuration & Environment Resolver
 */

(function () {
    const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const isLocalFile = window.location.protocol === 'file:';
    const isFlaskDirect = isLocalhost && window.location.port === '5000';

    const API_BASE = window.PRICEVANA_API_BASE
        || (isFlaskDirect ? '' : (isLocalhost || isLocalFile ? 'http://127.0.0.1:5000' : 'https://pricevana.onrender.com'));

    window.PRICEVANA_CONFIG = {
        API_BASE: API_BASE,
        isLocal: isLocalhost || isLocalFile,
        SUPPORTED_RETAILERS: ['Amazon', 'Flipkart', 'Myntra']
    };

    // Global alias for compatibility
    window.API_BASE = API_BASE;
})();
