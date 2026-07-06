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

        // Reset filter controls to defaults on fresh load
        searchInput.value = '';
        roleFilter.value = 'all';

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
    
    let imageContent = '';
    if (isPlaceholder) {
        imageContent = `
            <div class="placeholder-wrapper">
                <img src="/static/assets/placeholder.png" class="portfolio-image placeholder" alt="${portfolio.name}'s Portfolio" loading="lazy">
                <div class="placeholder-text">
                    <span class="placeholder-title">Preview Unavailable</span>
                    <span class="placeholder-sub">Please click open to view</span>
                </div>
            </div>
        `;
    } else {
        imageContent = `
            <div class="scroll-wrapper">
                <img src="${API_BASE}/api/screenshots/${portfolio.safe_name}_part1.jpg" class="portfolio-image" alt="Part 1" loading="lazy">
                <img src="${API_BASE}/api/screenshots/${portfolio.safe_name}_part2.jpg" class="portfolio-image" alt="Part 2" loading="lazy">
                <img src="${API_BASE}/api/screenshots/${portfolio.safe_name}_part3.jpg" class="portfolio-image" alt="Part 3" loading="lazy">
            </div>
        `;
    }

    card.innerHTML = `
        <div class="card-header">
            <div class="window-controls">
                <div class="control-dot"></div>
                <div class="control-dot"></div>
                <div class="control-dot"></div>
            </div>
            <h3 class="card-title" title="${escapeHtml(portfolio.name)}">${escapeHtml(portfolio.name)}</h3>
            <span class="role-badge" title="${escapeHtml(portfolio.role || 'Developer')}">${escapeHtml(portfolio.role || 'Developer')}</span>
        </div>
        <div class="card-image-window">
            ${imageContent}
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


// ─── Role Normalization (Curated Allowlist) ──────
// Only these categories appear in the dropdown. Everything else maps to null and is excluded.
const ROLE_RULES = [
    { label: 'AI/ML Engineer',          test: s => /\b(ai|ml|artificial intelligence|machine learning|gen.?ai|generative ai|nlp|llm|deep learning|computer vision)\b/.test(s) || s.includes('ai-') || s.includes('ai/ml') },
    { label: 'Frontend Developer',      test: s => /\b(frontend|front.?end|react|vue|angular|nextjs|next\.js|svelte|astro)\b/.test(s) },
    { label: 'Backend Developer',       test: s => /\b(backend|back.?end|node\.?js|express|django|flask|fastapi|spring.?boot|laravel|nestjs|php|golang|ruby on rails)\b/.test(s) },
    { label: 'Full Stack Developer',    test: s => /\b(full.?stack|fullstack|mern|mean|pern)\b/.test(s) },
    { label: 'Mobile Developer',        test: s => /\b(ios|android|mobile|flutter|react native|swift|kotlin|app dev)\b/.test(s) },
    { label: 'UI/UX Designer',          test: s => /\b(ui|ux|ui\/ux|ux\/ui|product design|graphic design|web design)\b/.test(s) },
    { label: 'DevOps / Cloud',          test: s => /\b(devops|cloud|aws|azure|gcp|docker|kubernetes|ci\/cd|sre|infrastructure|platform engineer)\b/.test(s) },
    { label: 'Data Science',            test: s => /\b(data sci|data engineer|data analyst|big data|pandas|numpy|matplotlib)\b/.test(s) },
    { label: 'Cyber Security',          test: s => /\b(cyber.?security|security|pentester|osint|devsecops|forensics)\b/.test(s) },
    { label: 'Web3 / Blockchain',       test: s => /\b(web3|blockchain|crypto|solidity|smart contract|ethereum)\b/.test(s) },
    { label: 'Game Developer',          test: s => /\b(game dev|game developer|unity|unreal|godot)\b/.test(s) },
    { label: 'Embedded / IoT',          test: s => /\b(embedded|iot|firmware|robotics|arduino|raspberry)\b/.test(s) },
    { label: 'Software Engineer',       test: s => /\b(software engineer|software developer|software development|swe|sde)\b/.test(s) },
    { label: 'Web Developer',           test: s => /\b(web dev|web developer|web programmer|webflow|wordpress|shopify)\b/.test(s) },
    { label: '.NET Developer',          test: s => /\b(\.net|dotnet|c#|blazor)\b/.test(s) },
    { label: 'Python Developer',        test: s => /\b(python)\b/.test(s) },
    { label: 'Java Developer',          test: s => /\b(java|springboot|spring boot)\b/.test(s) && !/javascript/.test(s) },
    { label: 'Developer',               test: s => /\b(developer|programmer|coder|engineer)\b/.test(s) },
    { label: 'Freelancer',              test: s => /\b(freelanc)\b/.test(s) },
    { label: 'Open Source Contributor',  test: s => /\b(open source|contributor)\b/.test(s) },
    { label: 'Tech Lead / Manager',     test: s => /\b(tech lead|technical lead|lead engineer|engineering leader|director|staff engineer|senior|architect|manager|founder|ceo|cto)\b/.test(s) },
    { label: 'Student',                 test: s => /\b(student|undergrad|intern|learning|aspiring)\b/.test(s) },
    { label: 'Researcher',              test: s => /\b(researcher|research)\b/.test(s) },
    { label: 'QA / Testing',            test: s => /\b(qa|testing|test engineer|automation)\b/.test(s) },
    { label: 'Digital Creator',         test: s => /\b(digital creator|content creator|digital market|photographer|creator|blogger)\b/.test(s) },
];

function normalizeRole(role) {
    if (!role) return null;
    let lower = role.toLowerCase().trim().replace(/[.,;:!?]$/, '');
    if (lower.length < 2) return null;

    for (const rule of ROLE_RULES) {
        if (rule.test(lower)) return rule.label;
    }
    return null; // Not a recognized role category
}

// ─── Role Filter Dropdown ────────────────────────
function extractRoles(roleString) {
    if (!roleString) return ['Developer'];

    // Remove parentheses and their contents
    const noParens = roleString.replace(/\s*\(.*?\)\s*/g, '');

    // Split by |, &, •, , OR / and + surrounded by spaces
    const splitRegex = /\s*[|&•,]\s*|\s+[\/+]\s+/;
    const roles = noParens.split(splitRegex)
        .map(r => normalizeRole(r))
        .filter(r => r !== null);

    return roles.length > 0 ? roles : ['Developer'];
}

function populateRoleFilter(portfolios) {
    const roles = new Set();
    portfolios.forEach(p => {
        const extracted = extractRoles(p.role);
        extracted.forEach(r => roles.add(r));
    });

    // Sort alphabetically
    const sorted = [...roles].sort((a, b) => a.localeCompare(b));

    sorted.forEach(role => {
        const option = document.createElement('option');
        option.value = role;
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
        
        const extractedRoles = extractRoles(p.role);
        const roleMatch = selectedRole === 'all' || extractedRoles.includes(selectedRole);
        
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

// ─── Scroll to Top Button ──────────────────────────
const scrollToTopBtn = document.getElementById('scroll-to-top');

window.addEventListener('scroll', () => {
    // Show button when scrolled down 500px
    if (window.scrollY > 500) {
        scrollToTopBtn.classList.remove('hidden');
    } else {
        scrollToTopBtn.classList.add('hidden');
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
