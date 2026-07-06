# `frontend/styles.css`

## Purpose
The global stylesheet for DevFolio, implementing a highly premium, Zayar Shein-inspired "Neo-Brutalist" design language.

## Recent Updates
1. **Card Overflow Fix**: Added `overflow: hidden` to both `.portfolio-card` and `.card-header` to prevent long role badges from breaking out of card boundaries.
2. **Role Badge Truncation**: The `.role-badge` now uses `text-overflow: ellipsis`, `overflow: hidden`, and `max-width: 55%` to cleanly truncate long multi-role strings within the card header. Full text is viewable via hover tooltip.
3. **Card Title Flex Constraints**: `.card-title` uses `flex: 1` and `min-width: 0` to properly share space with the role badge without either element overflowing.
4. **Grid Layout**: Uses `grid-template-columns: repeat(2, minmax(0, 1fr))` to prevent large screenshot images from blowing out the grid columns.
5. **Scroll Wrapper**: `.scroll-wrapper` holds 3 incremental screenshots. The `.portfolio-card:hover .scroll-wrapper` translates vertically upwards to create an automated scrolling effect on hover.
6. **Neo-Brutalist Theming**: Fully implemented CSS custom variables for Light and Dark modes. Light uses Manila tones; Dark uses the exact palette (`#1a0f09`, `#efe3cf`) scraped from `zayarshein.com`. Features thick borders, flat hard shadows, and a retro dot-matrix background.
7. **Placeholder Styling**: Absolute positioning classes overlay "Preview Unavailable" text crisply on top of the custom-generated Neo-Brutalist placeholder graphic.
8. **Scraper Progress Bar**: Styled progress bar with animated fill, matching the Neo-Brutalist theme with thick borders and flat shadows.
9. **Scroll to Top Button**: Fixed-position floating button with smooth show/hide transitions based on scroll position.
