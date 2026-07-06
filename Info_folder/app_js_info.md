# `frontend/app.js`

## Purpose
The core frontend logic file that handles fetching portfolio data, managing state, executing filters (by name and role), dynamically rendering UI components, and providing real-time scraper progress updates.

## Recent Updates
1. **Curated Role Normalization (Allowlist)**: Introduced a `ROLE_RULES` array of 25 curated role categories (e.g., AI/ML Engineer, Full Stack Developer, Frontend Developer). The `normalizeRole()` function maps every raw role string against these rules. Unrecognized roles (e.g., "Kenya", "GitHub Star", "8x Google Hall of Fame") return `null` and are excluded from the dropdown, keeping it clean and professional.
2. **Smart Role Splitting**: The `extractRoles()` function splits multi-role strings (e.g., `"Full Stack Developer | AI Engineer"`) by delimiters (`|`, `&`, `•`, `,`, and space-surrounded `/` or `+`), normalizes each fragment independently, and deduplicates them. Users with multiple roles appear under every matching category.
3. **Dynamic Card Updates**: Periodically polls `/api/portfolios` and uses DOM diffing to swap placeholder cards for real screenshot cards without re-rendering the entire grid.
4. **Real-time Scraper Progress Bar**: `updateProgressBar()` shows/hides a progress bar with percentage tracking based on the ratio of portfolios with screenshots.
5. **Filter Reset on Reload**: Explicitly resets the search input and role dropdown to defaults on page load to prevent stale browser-cached form values from causing empty grids.
6. **3-Screenshot Hover Effect**: Cards with screenshots stack 3 incremental images inside a `.scroll-wrapper` div. CSS translates the wrapper upwards on hover for an automated scrolling effect.
7. **Lazy Loading**: All 1,157+ dynamically injected image elements use `loading="lazy"` for performance.
8. **Tooltip Overflow Handling**: Both the card title and role badge include `title` attributes so users can hover to read truncated text.
9. **Theme Toggle**: Persistent dark mode toggle swapping the `dark` class on the `<html>` root and changing the moon/sun SVG icon.
10. **Scroll to Top Button**: Floating button appears after scrolling 500px, smooth-scrolls back to top on click.
