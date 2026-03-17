// ============================================
// CONFIG & CONSTANTS
// ============================================
const API_ENDPOINT = localStorage.getItem('apiEndpoint') || 'http://localhost:8000';
const STORAGE_KEY_HISTORY = 'dashboardHistory';
const STORAGE_KEY_SETTINGS = 'dashboardSettings';

// ============================================
// STATE MANAGEMENT
// ============================================
let currentQuery = '';
let queryHistory = JSON.parse(localStorage.getItem(STORAGE_KEY_HISTORY)) || [];
let settings = JSON.parse(localStorage.getItem(STORAGE_KEY_SETTINGS)) || {
    theme: 'light',
    autoRefresh: false,
};

let charts = {};

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    updateRecentQueries();
    updateHistoryList();
    applyTheme();
    checkAPIStatus();
});

// ============================================
// EVENT LISTENERS
// ============================================
function initializeEventListeners() {
    // Tab Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const tabName = item.dataset.tab;
            switchTab(tabName);
        });
    });

    // Menu Toggle (Mobile)
    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            document.querySelector('.sidebar').classList.toggle('active');
        });
    }

    // Theme Selection
    const themeSelect = document.getElementById('themeSelect');
    if (themeSelect) {
        themeSelect.addEventListener('change', (e) => {
            settings.theme = e.target.value;
            saveSettings();
            applyTheme();
        });
    }

    // Query Input
    const queryInput = document.getElementById('queryInput');
    if (queryInput) {
        queryInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                submitQuery();
            }
        });
    }
}

// ============================================
// TAB NAVIGATION
// ============================================
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    // Show selected tab
    const tab = document.getElementById(tabName);
    if (tab) {
        tab.classList.add('active');
    }

    // Mark nav item as active
    const navItem = document.querySelector(`.nav-item[data-tab="${tabName}"]`);
    if (navItem) {
        navItem.classList.add('active');
    }

    // Update page title
    const pageTitle = document.querySelector('.page-title');
    if (pageTitle) {
        const titles = {
            'dashboard': 'Dashboard',
            'query': 'Query Builder',
            'history': 'History',
            'settings': 'Settings'
        };
        pageTitle.textContent = titles[tabName] || 'Dashboard';
    }

    // Close mobile sidebar after tab switch
    document.querySelector('.sidebar').classList.remove('active');
}

// ============================================
// QUERY BUILDER
// ============================================
function setQuery(query) {
    document.getElementById('queryInput').value = query;
    switchTab('query');
}

function clearQuery() {
    document.getElementById('queryInput').value = '';
    document.getElementById('rowLimit').value = '100';
    document.getElementById('filterInput').value = '';
}

function fillExample() {
    document.getElementById('queryInput').value = 'Show me the total revenue by month in the last year';
}

async function submitQuery() {
    const queryInput = document.getElementById('queryInput');
    currentQuery = queryInput.value.trim();

    if (!currentQuery) {
        showToast('Please enter a query', 'error');
        return;
    }

    const dataSource = document.getElementById('dataSource').value;
    const rowLimit = parseInt(document.getElementById('rowLimit').value) || 100;
    const filters = document.getElementById('filterInput').value.trim();

    // Show loading state
    const resultsArea = document.getElementById('resultsArea');
    const loadingState = document.getElementById('loadingState');
    const chartsContainer = document.getElementById('chartsContainer');
    const tableContainer = document.getElementById('tableContainer');
    const insightsContainer = document.getElementById('insightsContainer');
    const errorState = document.getElementById('errorState');

    resultsArea.style.display = 'block';
    loadingState.style.display = 'flex';
    chartsContainer.style.display = 'none';
    tableContainer.style.display = 'none';
    insightsContainer.style.display = 'none';
    errorState.style.display = 'none';

    try {
        const payload = {
            query: currentQuery,
            data_source: dataSource || undefined,
            limit: rowLimit,
            filters: filters ? JSON.parse(`{${filters}}`) : {}
        };

        const response = await fetch(`${API_ENDPOINT}/api/dashboard/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();

        // Hide loading, show results
        loadingState.style.display = 'none';

        // Add to history
        addToHistory(currentQuery);

        // Display charts
        if (data.charts && data.charts.length > 0) {
            displayCharts(data.charts);
            chartsContainer.style.display = 'grid';
        }

        // Display data table
        if (data.data && data.data.length > 0) {
            displayTable(data.data);
            tableContainer.style.display = 'block';
        }

        // Display insights
        if (data.insights && data.insights.length > 0) {
            displayInsights(data.insights);
            insightsContainer.style.display = 'block';
        }

        showToast('Dashboard generated successfully!', 'success');

    } catch (error) {
        console.error('Query Error:', error);
        loadingState.style.display = 'none';
        errorState.style.display = 'flex';
        document.getElementById('errorMessage').textContent = error.message || 'Failed to generate dashboard';
        showToast('Error generating dashboard', 'error');
    }
}

// ============================================
// CHART DISPLAY
// ============================================
function displayCharts(charts) {
    const container = document.getElementById('chartsContainer');
    container.innerHTML = '';

    charts.forEach((chartData, index) => {
        const chartBox = document.createElement('div');
        chartBox.className = 'chart-box';

        const title = document.createElement('div');
        title.className = 'chart-title';
        title.textContent = chartData.title || `Chart ${index + 1}`;

        const canvas = document.createElement('canvas');
        canvas.id = `chart-${index}`;
        canvas.style.maxHeight = '300px';

        chartBox.appendChild(title);
        chartBox.appendChild(canvas);
        container.appendChild(chartBox);

        // Create chart using Chart.js
        setTimeout(() => {
            try {
                new Chart(canvas, {
                    type: chartData.type || 'bar',
                    data: {
                        labels: chartData.labels || [],
                        datasets: [{
                            label: chartData.series_name || 'Data',
                            data: chartData.values || [],
                            backgroundColor: getChartColors(chartData.type),
                            borderColor: getChartBorderColor(chartData.type),
                            borderWidth: chartData.type === 'pie' ? 0 : 1,
                            tension: 0.4,
                            fill: chartData.type === 'line' ? true : false,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                            }
                        },
                        scales: chartData.type === 'pie' ? {} : {
                            y: {
                                beginAtZero: true,
                            }
                        }
                    }
                });
            } catch (e) {
                console.error('Chart rendering error:', e);
            }
        }, 0);
    });
}

function getChartColors(type) {
    const colors = [
        'rgba(99, 102, 241, 0.6)',
        'rgba(236, 72, 153, 0.6)',
        'rgba(16, 185, 129, 0.6)',
        'rgba(245, 158, 11, 0.6)',
        'rgba(239, 68, 68, 0.6)',
    ];

    if (type === 'pie') {
        return colors;
    }
    return colors[0];
}

function getChartBorderColor(type) {
    const colors = [
        'rgb(99, 102, 241)',
        'rgb(236, 72, 153)',
        'rgb(16, 185, 129)',
        'rgb(245, 158, 11)',
        'rgb(239, 68, 68)',
    ];
    return colors[0];
}

// ============================================
// TABLE DISPLAY
// ============================================
function displayTable(data) {
    const table = document.getElementById('dataTable');
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');

    // Clear existing
    thead.innerHTML = '';
    tbody.innerHTML = '';

    if (!data || data.length === 0) return;

    // Get columns from first row
    const columns = Object.keys(data[0]);

    // Create header
    const headerRow = document.createElement('tr');
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Create rows (limit to first 50)
    data.slice(0, 50).forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            const value = row[col];
            td.textContent = value !== null ? value : '—';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    // Show message if limited
    if (data.length > 50) {
        const msgRow = document.createElement('tr');
        const msgCell = document.createElement('td');
        msgCell.colSpan = columns.length;
        msgCell.textContent = `Showing 50 of ${data.length} rows`;
        msgCell.style.textAlign = 'center';
        msgCell.style.color = 'var(--text-secondary)';
        msgCell.style.padding = '15px';
        msgCell.style.fontStyle = 'italic';
        tbody.appendChild(msgRow);
    }
}

// ============================================
// INSIGHTS DISPLAY
// ============================================
function displayInsights(insights) {
    const container = document.getElementById('insightsList');
    container.innerHTML = '';

    insights.forEach(insight => {
        const item = document.createElement('div');
        item.className = 'insight-item';
        item.innerHTML = `<strong>•</strong> ${insight}`;
        container.appendChild(item);
    });
}

// ============================================
// RESULTS MANAGEMENT
// ============================================
function closeResults() {
    document.getElementById('resultsArea').style.display = 'none';
    clearQuery();
}

// ============================================
// HISTORY MANAGEMENT
// ============================================
function addToHistory(query) {
    const historyItem = {
        id: Date.now(),
        query: query,
        timestamp: new Date().toLocaleString()
    };

    queryHistory.unshift(historyItem);
    if (queryHistory.length > 20) {
        queryHistory = queryHistory.slice(0, 20);
    }

    localStorage.setItem(STORAGE_KEY_HISTORY, JSON.stringify(queryHistory));
    updateHistoryList();
    updateRecentQueries();
}

function updateHistoryList() {
    const historyList = document.getElementById('historyList');

    if (!historyList) return;

    if (queryHistory.length === 0) {
        historyList.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📭</span>
                <p>No query history yet</p>
            </div>
        `;
        return;
    }

    historyList.innerHTML = queryHistory.map(item => `
        <div class="history-item">
            <div class="history-query">${escapeHtml(item.query)}</div>
            <div class="history-timestamp">${item.timestamp}</div>
            <div style="margin-top: 10px;">
                <button class="btn-example" onclick="setQuery('${escapeHtml(item.query).replace(/'/g, "\\'")}')">
                    Use Query
                </button>
                <button class="btn-clear" onclick="deleteHistoryItem(${item.id})">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}

function deleteHistoryItem(id) {
    queryHistory = queryHistory.filter(item => item.id !== id);
    localStorage.setItem(STORAGE_KEY_HISTORY, JSON.stringify(queryHistory));
    updateHistoryList();
}

function updateRecentQueries() {
    const recentList = document.getElementById('recentList');
    if (!recentList) return;

    if (queryHistory.length === 0) {
        recentList.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📭</span>
                <p>No recent queries yet. Start by asking a question!</p>
            </div>
        `;
        return;
    }

    recentList.innerHTML = queryHistory.slice(0, 5).map(item => `
        <div style="padding: 10px; background: var(--light-darker); border-radius: 6px; cursor: pointer;" 
             onclick="setQuery('${escapeHtml(item.query).replace(/'/g, "\\'")}')" title="${item.timestamp}">
            <strong>${escapeHtml(item.query.substring(0, 50))}${item.query.length > 50 ? '...' : ''}</strong>
            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 5px;">
                ${new Date(item.timestamp).toLocaleDateString()}
            </div>
        </div>
    `).join('');
}

// ============================================
// SETTINGS
// ============================================
function saveSettings() {
    settings.theme = document.getElementById('themeSelect')?.value || 'light';
    settings.autoRefresh = document.getElementById('autoRefresh')?.checked || false;

    const apiEndpoint = document.getElementById('apiEndpoint')?.value;
    if (apiEndpoint) {
        localStorage.setItem('apiEndpoint', apiEndpoint);
    }

    localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(settings));
    showToast('Settings saved successfully!', 'success');
}

// ============================================
// THEME
// ============================================
function applyTheme() {
    const theme = settings.theme;
    const html = document.documentElement;

    if (theme === 'dark') {
        html.style.colorScheme = 'dark';
    } else if (theme === 'light') {
        html.style.colorScheme = 'light';
    } else {
        html.style.colorScheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
}

// ============================================
// API STATUS CHECK
// ============================================
async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_ENDPOINT}/`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            const statusIndicator = document.querySelector('.status-indicator');
            if (statusIndicator) {
                statusIndicator.classList.add('online');
            }
        }
    } catch (error) {
        console.log('API Status: Offline');
    }
}

// ============================================
// NOTIFICATIONS
// ============================================
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ============================================
// MODAL
// ============================================
function showModal(title, message) {
    const modal = document.getElementById('modal');
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').textContent = message;
    modal.style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Click outside modal to close
document.addEventListener('click', (e) => {
    const modal = document.getElementById('modal');
    if (e.target === modal) {
        closeModal();
    }
});

// ============================================
// UTILITY FUNCTIONS
// ============================================
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ============================================
// RESPONSIVE BEHAVIOR
// ============================================
document.addEventListener('click', (e) => {
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.getElementById('menuToggle');

    if (!sidebar || !menuToggle) return;

    // Close sidebar when clicking outside (on mobile)
    if (window.innerWidth <= 600 && 
        sidebar.classList.contains('active') &&
        !sidebar.contains(e.target) &&
        !menuToggle.contains(e.target)) {
        sidebar.classList.remove('active');
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 600) {
        document.querySelector('.sidebar').classList.remove('active');
    }
});

// ============================================
// KEYBOARD SHORTCUTS
// ============================================
document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+Q: Focus query input
    if (e.ctrlKey && e.shiftKey && e.key === 'Q') {
        const queryInput = document.getElementById('queryInput');
        if (queryInput) {
            queryInput.focus();
            switchTab('query');
        }
    }

    // Escape: Close results
    if (e.key === 'Escape') {
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea && resultsArea.style.display !== 'none') {
            closeResults();
        }
    }
});

// ============================================
// PERFORMANCE OPTIMIZATION
// ============================================
// Lazy load charts
const observerOptions = {
    threshold: 0.1
};

if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.chart-box').forEach(box => {
        observer.observe(box);
    });
}
