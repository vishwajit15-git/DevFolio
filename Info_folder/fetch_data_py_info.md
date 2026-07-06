# fetch_data.py — Data Fetcher & Parser

## File Path
`backend/fetch_data.py`

## Purpose
Downloads the `feed.json` file from the `emmabostian/developer-portfolios` GitHub repository, filters out excluded portfolios via `excluded_names.py`, and parses the remaining entries to extract portfolio data. Each entry contains a developer name, portfolio URL, and a `tagline` field that holds the job role.

## Dependencies
- `requests` — HTTP library to download `feed.json` from GitHub's raw content URL
- `excluded_names.EXCLUDED_NAMES` — Set of 149 developer names to exclude from the dataset

## Connection to Other Files
- **Imports from** `excluded_names.py` → uses `EXCLUDED_NAMES` set to filter out unwanted portfolios
- **Consumed by** `main.py` → the `/api/portfolios` endpoint calls `get_portfolio_data()`
- **Data feeds into** `screenshot_service.py` → provides the list of portfolio URLs to screenshot

## Constants

| Name | Value | Purpose |
|---|---|---|
| `FEED_URL` | `https://raw.githubusercontent.com/emmabostian/developer-portfolios/master/feed.json` | Raw GitHub URL for the upstream data source |

## Functions

### `get_portfolio_data() → list[dict]`
Fetches `feed.json`, filters out excluded names, parses each remaining entry, and returns a capped list of cleaned portfolio dictionaries.

**Returns:** A list of dicts (max 1,157), each containing:
- `name` (str) — Developer name
- `role` (str) — Job title from the `tagline` field, defaults to `"Developer"` if absent
- `url` (str) — Portfolio URL

**Filtering Pipeline:**
1. Fetch all ~1,806 entries from GitHub
2. Skip any entry whose `name` is in `EXCLUDED_NAMES` (149 entries)
3. Cap the result at 1,157 entries (previously 1,306, reduced after bulk deletion)

**Error handling:** Catches `requests.exceptions.RequestException`, logs the error, and returns an empty list.

## Key Implementation Details

### Excluded Names Import
Uses a try/except chain to import `EXCLUDED_NAMES` from either `backend.excluded_names` (when run via `uvicorn backend.main:app`) or `excluded_names` (when run directly). Falls back to an empty set if neither import succeeds.

```python
try:
    from backend.excluded_names import EXCLUDED_NAMES
except ImportError:
    try:
        from excluded_names import EXCLUDED_NAMES
    except ImportError:
        EXCLUDED_NAMES = set()
```

### Dataset Capping
The dataset is capped at 1,157 entries to optimize scraper performance and exclude heavy/dead portfolio links:
```python
return cleaned_portfolios[:1157]
```

---
*Last Updated: 2026-07-06 (Added excluded names filtering, reduced dataset cap from 1,306 to 1,157)*
