/**
 * DevFolio - Frontend Application
 * Fetches portfolio data from the Python backend and renders the interactive card grid.
 * Implements search filtering, role-based dropdown filtering, and hover-to-scroll previews.
 */

const API_BASE = window.location.origin;
let allPortfolios = [];

// ─── DOM References ──────────────────────────────
const grid = document.getElementById('gallery-grid');
const searchInput = document.getElementById('search-input');
const roleFilter = document.getElementById('role-filter');
const loadingOverlay = document.getElementById('loading-overlay');
const portfolioCountEl = document.getElementById('portfolio-count');
const visibleCountEl = document.getElementById('visible-count');


// ─── Fetch & Initialize ──────────────────────────
async function loadPortfolios() {
    try {
        const response = await fetch(`${API_BASE}/api/portfolios`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        allPortfolios = data.portfolios;
        portfolioCountEl.textContent = data.count.toLocaleString();

        // Populate the role dropdown with unique roles
        populateRoleFilter(allPortfolios);

        // Render the initial grid
        renderGrid(allPortfolios);

        // Hide the loading overlay
        loadingOverlay.classList.add('hidden');
        setTimeout(() => { loadingOverlay.style.display = 'none'; }, 500);

    } catch (error) {
        console.error('Error loading gallery:', error);
        grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:#9898a8;padding:60px 20px;font-size:15px;">
            Failed to load portfolios. Make sure the backend server is running on <code>uvicorn</code>.
        </p>`;
        loadingOverlay.classList.add('hidden');
    }
}


// ─── Render Grid ─────────────────────────────────
function renderGrid(portfolios) {
    grid.innerHTML = '';

    if (portfolios.length === 0) {
        grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:#9898a8;padding:60px 20px;font-size:15px;">
            No portfolios match your search.
        </p>`;
        visibleCountEl.textContent = '0';
        return;
    }

    portfolios.forEach(portfolio => {
        const card = createCard(portfolio);
        grid.appendChild(card);
    });

    visibleCountEl.textContent = portfolios.length.toLocaleString();
}


// ─── Create a Single Card ────────────────────────
function createCard(portfolio) {
    const card = document.createElement('div');
    card.className = 'portfolio-card';
    card.dataset.name = portfolio.name.toLowerCase();
    card.dataset.role = (portfolio.role || 'Developer').toLowerCase();

    // Determine image source: real screenshot or fallback placeholder
    const isPlaceholder = !portfolio.has_screenshots;
    const imageSrc = isPlaceholder
        ? '/static/assets/placeholder.png'
        : `${API_BASE}/screenshots/${portfolio.safe_name}_part1.png`;

    const placeholderClass = isPlaceholder ? ' placeholder' : '';

    card.innerHTML = `
        <div class="card-header">
            <div class="window-controls">
                <div class="control-dot"></div>
                <div class="control-dot"></div>
                <div class="control-dot"></div>
            </div>
            <h3 class="card-title">${escapeHtml(portfolio.name)}</h3>
            <span class="role-badge">${escapeHtml(portfolio.role || 'Developer')}</span>
        </div>
        <div class="card-image-window">
            <img
                src="${imageSrc}"
                class="portfolio-image${placeholderClass}"
                alt="${portfolio.name}'s Portfolio"
                loading="lazy"
            >
            <div class="visit-btn-wrapper">
                <a href="${portfolio.url}" target="_blank" rel="noopener noreferrer" class="visit-link">
                    Open
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                        <path d="M5 12h14M12 5l7 7-7 7"/>
                    </svg>
                </a>
            </div>
        </div>
    `;

    // Clicking the card (not the link) also opens the portfolio
    card.addEventListener('click', (e) => {
        if (e.target.tagName !== 'A') {
            window.open(portfolio.url, '_blank', 'noopener');
        }
    });

    return card;
}


// ─── Role Filter Dropdown ────────────────────────
function populateRoleFilter(portfolios) {
    const roles = new Set();
    portfolios.forEach(p => {
        const role = (p.role || 'Developer').trim();
        if (role && role.length < 40) roles.add(role);
    });

    // Sort alphabetically
    const sorted = [...roles].sort((a, b) => a.localeCompare(b));

    sorted.forEach(role => {
        const option = document.createElement('option');
        option.value = role.toLowerCase();
        option.textContent = role;
        roleFilter.appendChild(option);
    });
}


// ─── Filter Logic ────────────────────────────────
function applyFilters() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedRole = roleFilter.value;

    const filtered = allPortfolios.filter(p => {
        const nameMatch = p.name.toLowerCase().includes(searchTerm);
        const roleMatch = selectedRole === 'all' || (p.role || 'Developer').toLowerCase() === selectedRole;
        return nameMatch && roleMatch;
    });

    renderGrid(filtered);
}

// Debounced search for performance with 1,800+ entries
let searchTimeout;
searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(applyFilters, 250);
});

roleFilter.addEventListener('change', applyFilters);


// ─── Utilities ───────────────────────────────────
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// ─── Theme Toggle ──────────────────────────────────
const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    
    // Swap icon based on theme
    themeToggle.innerHTML = isDark 
        ? `<svg class="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
               <circle cx="12" cy="12" r="5"></circle>
               <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
           </svg>`
        : `<svg class="moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
               <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>
           </svg>`;
});

// ─── Boot ────────────────────────────────────────
document.addEventListener('DOMContentLoaded', loadPortfolios);
