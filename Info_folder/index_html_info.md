# index.html — Frontend Entry Point

## File Path
`frontend/index.html`

## Purpose
The main HTML document that serves as the shell for the DevFolio single-page application. Contains the root `<div id="app">` container where JavaScript dynamically renders the portfolio grid cards.

## Dependencies
- `styles.css` — Linked stylesheet for 2×2 grid layout and hover animations
- `app.js` — Linked script that fetches data and renders cards into the `#app` div

## Connection to Other Files
- **Links to** `styles.css` → all visual styling
- **Links to** `app.js` → all interactivity and data rendering
- **Receives data from** `backend/main.py` → via `app.js` fetch calls to the FastAPI server

## Line-by-Line Explanation

```html
<!-- Line 1 -->
<!DOCTYPE html>
```
- Declares this as an HTML5 document, ensuring modern standards-mode rendering.

```html
<!-- Line 2 -->
<html lang="en">
```
- Root HTML element with `lang="en"` for accessibility and SEO (tells browsers/screen readers the page is in English).

```html
<!-- Lines 3-8: Head section -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="DevFolio - A visual gallery of 1,800+ developer portfolios for design and coding inspiration.">
    <title>DevFolio | Developer Portfolio Gallery</title>
    <link rel="stylesheet" href="styles.css">
</head>
```
- **Line 4:** Sets character encoding to UTF-8 (supports all international characters).
- **Line 5:** Viewport meta tag for responsive design on mobile devices.
- **Line 6:** SEO meta description — appears in search engine results.
- **Line 7:** Page title — shown in the browser tab and search results.
- **Line 8:** Links the external CSS stylesheet.

```html
<!-- Lines 9-13: Body section -->
<body>
    <div id="app"></div>
    <script src="app.js"></script>
</body>
</html>
```
- **Line 10:** Empty `#app` div — JavaScript will inject the entire portfolio grid here.
- **Line 11:** Loads `app.js` at the end of body so the DOM is ready before the script runs.

---
*Last Updated: 2026-07-01 (Day 1 — Initial scaffold)*
