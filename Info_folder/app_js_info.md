# app.js — Frontend Application Logic

## File Path
`frontend/app.js`

## Purpose
The main JavaScript file that powers the DevFolio frontend. Responsible for:
1. Fetching portfolio data from the Python backend API (`/api/portfolios`)
2. Dynamically rendering portfolio cards into the `#app` grid container
3. Implementing lazy-loading (Intersection Observer) for performance
4. Handling the hover-to-scroll animation (translating the screenshot image upward on hover)
5. Managing the job-title filter UI (parsing bracketed titles for role-based sorting)

## Dependencies
- Browser `fetch` API — for requesting data from the FastAPI backend
- Browser `IntersectionObserver` API — for lazy-loading cards as they enter the viewport
- DOM APIs — for creating and manipulating card elements

## Connection to Other Files
- **Loaded by** `index.html` → `<script src="app.js">`
- **Fetches data from** `backend/main.py` → API endpoints serving portfolio JSON and screenshot URLs
- **Creates elements styled by** `styles.css` → card elements use CSS classes for layout and animation

## Functions / Classes
*(Currently a placeholder — will be updated as code is written)*

## Line-by-Line Explanation

```javascript
// Lines 1-4: File header comment
/**
 * DevFolio - Frontend Application
 * Fetches portfolio data from the Python backend and renders the interactive card grid.
 */
```
- **Lines 1–4:** A JSDoc-style block comment describing the file's responsibility — data fetching and card rendering.

---
*Last Updated: 2026-07-01 (Day 1 — Initial scaffold)*
