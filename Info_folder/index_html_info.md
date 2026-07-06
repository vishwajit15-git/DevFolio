# `frontend/index.html`

## Purpose
The primary HTML document serving the DevFolio frontend.

## Recent Updates
1. **Container Alignment**: Wrapped the `#hero-header`, `#filter-bar`, and `.gallery-grid` inside a global `<div class="container">`. This perfectly synchronizes their max-widths to `1400px` without edge clipping or horizontal alignment issues.
2. **Neo-Brutalist Layout**: Uses a retro-window structure with macOS-style window controls (three dots) in the header.
3. **Scraper Progress Bar**: Added a collapsible progress bar section (`#scraper-progress-container`) that displays real-time scraper progress with a percentage counter and animated fill bar. Auto-hides when all screenshots are complete.
4. **Role Filter Dropdown**: A `<select>` element (`#role-filter`) dynamically populated by `app.js` with 25 curated role categories. Defaults to "All Roles".
5. **Search Input**: Text input (`#search-input`) for filtering portfolios by developer name with debounced input handling.
6. **Stats Badge**: Shows the count of currently visible portfolios (`#visible-count`).
7. **Theme Toggle Button**: Dedicated button to switch between Manila Paper (light) and Dark Espresso (dark) themes.
8. **Scroll to Top Button**: A floating `#scroll-to-top` button with a Font Awesome arrow icon that appears after scrolling 500px.
9. **Cache-Busted Assets**: Static assets (`styles.css` and `app.js`) use `?v=N` query parameters to force browser cache invalidation after code updates.
10. **SEO Metadata**: Includes descriptive `<title>`, `<meta name="description">`, and proper heading hierarchy.
