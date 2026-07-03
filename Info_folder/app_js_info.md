# `frontend/app.js`

## Purpose
This is the core frontend logic file that handles fetching portfolio data, managing state, executing filters (by name and role), and dynamically rendering the UI components.

## Recent Updates
1. **Neo-Brutalist Placeholders**: Added a `placeholder-wrapper` with descriptive "Preview Unavailable" text that sits over the newly generated Neo-Brutalist `placeholder.png`.
2. **5-Screenshot Hover Effect**: Modified the `createCard` function so that if screenshots exist, it stacks 5 incremental screenshots inside a `.scroll-wrapper` div instead of just loading a single image. This allows CSS to translate the entire wrapper upwards on hover for a scrolling effect.
3. **Lazy Loading**: Maintained `loading="lazy"` on all 1,800+ dynamically injected image elements for massive performance gains.
4. **Theme Toggle**: Contains the logic for the persistent dark mode toggle (swapping the `dark` class on the `<html>` root element and changing the moon/sun SVG).
