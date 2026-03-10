// Main JavaScript for Análise Indra Application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeAnimations();
    initializeTooltips();
    initializeDashboard();
});

// Animation initialization
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Dashboard specific functionality
function initializeDashboard() {
    // Auto-refresh dashboard data (mock implementation)
    if (document.querySelector('#dashboardTabs')) {
        // Update dashboard every 30 seconds (for demo purposes)
        setInterval(updateDashboardData, 30000);
    }

    // Add click tracking for tabs
    const tabs = document.querySelectorAll('#dashboardTabs .nav-link');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabName = this.id.replace('-tab', '');
            trackTabClick(tabName);
        });
    });
}

// Mock function to update dashboard data
function updateDashboardData() {
    // This would normally fetch new data from the server
    console.log('Dashboard data updated at', new Date().toLocaleTimeString());

    // Add a subtle refresh indicator
    const refreshIndicator = document.createElement('div');
    refreshIndicator.className = 'position-fixed top-50 end-0 p-3';
    refreshIndicator.innerHTML = `
        <div class="toast align-items-center text-white bg-success border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-check-circle me-2"></i>
                    Dados atualizados
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(refreshIndicator);

    const toast = new bootstrap.Toast(refreshIndicator.querySelector('.toast'));
    toast.show();

    setTimeout(() => {
        document.body.removeChild(refreshIndicator);
    }, 3000);
}

// Track tab clicks for analytics
function trackTabClick(tabName) {
    console.log(`Tab clicked: ${tabName}`);
    // Here you would send analytics data to your tracking service
}

// Utility functions
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatPercentage(value) {
    return `${value.toFixed(1)}%`;
}

function formatNumber(value) {
    return new Intl.NumberFormat('pt-BR').format(value);
}

// Loading state management
function showLoading(button, text = 'Processando...') {
    button.disabled = true;
    button.innerHTML = `<i class="bi bi-hourglass-split"></i> ${text}`;
}

function hideLoading(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}

// File upload validation
function validateFile(file) {
    const allowedTypes = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!allowedTypes.includes(file.type)) {
        return { valid: false, error: 'Apenas arquivos XLS ou XLSX são permitidos.' };
    }

    if (file.size > maxSize) {
        return { valid: false, error: 'O arquivo deve ter no máximo 10MB.' };
    }

    return { valid: true };
}

// Drag and drop functionality for file upload
function initializeDragDrop() {
    const dropzone = document.querySelector('.dropzone');
    const fileInput = document.querySelector('#fileInput');

    if (!dropzone || !fileInput) return;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropzone.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropzone.classList.add('dragover');
    }

    function unhighlight() {
        dropzone.classList.remove('dragover');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            // Trigger change event
            fileInput.dispatchEvent(new Event('change'));
        }
    }
}

// Initialize drag and drop on upload page
if (document.querySelector('.dropzone')) {
    initializeDragDrop();
}

// Error handling
function showError(message) {
    const errorToast = document.querySelector('#errorToast');
    if (errorToast) {
        document.querySelector('#errorMessage').textContent = message;
        const toast = new bootstrap.Toast(errorToast);
        toast.show();
    } else {
        alert(message); // Fallback
    }
}

function showSuccess(message) {
    const successToast = document.querySelector('#successToast');
    if (successToast) {
        document.querySelector('#successMessage').textContent = message;
        const toast = new bootstrap.Toast(successToast);
        toast.show();
    } else {
        alert(message); // Fallback
    }
}

// Chart initialization (placeholder for future chart implementation)
function initializeCharts() {
    // This would initialize Chart.js or similar charting library
    console.log('Charts initialized');
}

// Responsive navigation
function initializeResponsiveNav() {
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
}

// Initialize responsive navigation
initializeResponsiveNav();

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + U to go to upload page
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        window.location.href = '/'; // Upload page
    }

    // Ctrl/Cmd + D to go to dashboard
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        window.location.href = '/dashboard/'; // Dashboard page
    }
});

// Performance monitoring
function logPerformance() {
    if ('performance' in window && 'timing' in performance) {
        const timing = performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);
    }
}

// Log performance on page load
window.addEventListener('load', logPerformance);

// Export functions for potential use in other scripts
window.AnaliseIndra = {
    formatCurrency,
    formatPercentage,
    formatNumber,
    showLoading,
    hideLoading,
    showError,
    showSuccess,
    validateFile
};