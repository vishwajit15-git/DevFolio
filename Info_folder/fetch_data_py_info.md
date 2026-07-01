# fetch_data.py — Data Fetcher & Parser

## File Path
`backend/fetch_data.py`

## Purpose
Downloads the `feed.json` file from the `emmabostian/developer-portfolios` GitHub repository and parses it to extract portfolio entries (developer name, URL, and bracketed job title).

## Dependencies
- `requests` — HTTP library to download `feed.json` from GitHub
- `json` (stdlib) — Parse the JSON response
- `re` (stdlib) — Regex to extract bracketed job titles like `[Software Engineer]`

## Connection to Other Files
- **Consumed by** `main.py` → the server imports parsed data from this module to serve via API
- **Data feeds into** `screenshot_service.py` → provides the list of portfolio URLs to screenshot

## Functions / Classes
*(Currently a placeholder — will be updated as code is written)*

## Line-by-Line Explanation

```python
# Line 1-4: Module docstring
"""
DevFolio Backend - Data Fetcher
Downloads and parses the feed.json file from the emmabostian/developer-portfolios repository.
"""
```
- **Lines 1–4:** Module-level docstring describing this file's responsibility — fetching and parsing the upstream data source.

---
*Last Updated: 2026-07-01 (Day 1 — Initial scaffold)*
