# `frontend/styles.css`

## Purpose
The global stylesheet for DevFolio, implementing a highly premium, Zayar Shein-inspired "Neo-Brutalist" design language.

## Recent Updates
1. **Grid Blowout Fix**: Updated the 2-column layout to use `grid-template-columns: repeat(2, minmax(0, 1fr))` to prevent large screenshot images from blowing out the grid columns.
2. **Scroll Wrapper**: Added CSS for `.scroll-wrapper` which holds 5 incremental screenshots. The `.portfolio-card:hover .scroll-wrapper` now translates vertically upwards to create an automated scrolling effect on hover.
3. **Neo-Brutalist Theming**: Fully implemented CSS custom variables for Light and Dark modes. Light uses Manila tones; Dark uses the exact palette (`#1a0f09`, `#efe3cf`) scraped from `zayarshein.com`. Features thick borders, flat hard shadows, and a retro dot-matrix background.
4. **Placeholder Styling**: Added absolute positioning classes to overlay "Preview Unavailable" text crisply on top of the custom-generated Neo-Brutalist placeholder graphic.
