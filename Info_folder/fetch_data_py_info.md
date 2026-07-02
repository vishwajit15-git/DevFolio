# fetch_data.py — Data Fetcher & Parser

## File Path
`backend/fetch_data.py`

## Purpose
Downloads the `feed.json` file from the `emmabostian/developer-portfolios` GitHub repository and parses it to extract portfolio entries. Each entry contains a developer name, portfolio URL, and a `tagline` field that holds the job role (e.g., `"Software Engineer"`, `"AI Engineer"`).

## Dependencies
- `requests` — HTTP library to download `feed.json` from GitHub's raw content URL

## Connection to Other Files
- **Consumed by** `main.py` → the `/api/portfolios` endpoint calls `get_portfolio_data()`
- **Data feeds into** `screenshot_service.py` → provides the list of portfolio URLs to screenshot

## Constants

| Name | Value | Purpose |
|---|---|---|
| `FEED_URL` | `https://raw.githubusercontent.com/emmabostian/developer-portfolios/master/feed.json` | Raw GitHub URL for the upstream data source |

## Functions

### `get_portfolio_data() → list[dict]`
Fetches `feed.json`, parses each entry, and returns a list of cleaned portfolio dictionaries.

**Returns:** A list of dicts, each containing:
- `name` (str) — Developer name
- `role` (str) — Job title from the `tagline` field, defaults to `"Developer"` if absent
- `url` (str) — Portfolio URL

**Error handling:** Catches `requests.exceptions.RequestException`, logs the error, and returns an empty list.

## Line-by-Line Explanation

```python
# Lines 1-5: Module docstring
"""
DevFolio Backend - Data Fetcher
Downloads and parses the feed.json file from the emmabostian/developer-portfolios repository.
Extracts developer names, portfolio URLs, and tagline-based job roles.
"""
```
- **Lines 1–5:** Module-level docstring. Updated to reflect that roles come from the `tagline` field, not bracketed text.

```python
# Line 7: Import
import requests
```
- **Line 7:** Imports `requests` for HTTP calls. Note: `re` (regex) was removed — the actual `feed.json` stores roles in a dedicated `tagline` field, so regex parsing is unnecessary.

```python
# Lines 9-10: Constant
FEED_URL = "https://raw.githubusercontent.com/emmabostian/developer-portfolios/master/feed.json"
```
- **Lines 9–10:** Module-level constant for the raw GitHub URL. Points to the `master` branch of the source repository.

```python
# Lines 13-23: Function definition & docstring
def get_portfolio_data():
    """..."""
```
- **Line 13:** Main function — no parameters needed since the URL is a constant.
- **Lines 14–22:** Docstring explaining return format and defaults.

```python
# Lines 24-26: HTTP request
    try:
        response = requests.get(FEED_URL, timeout=15)
        response.raise_for_status()
```
- **Line 24:** `try` block wraps all network operations.
- **Line 25:** GET request with 15-second timeout to prevent indefinite hanging.
- **Line 26:** `raise_for_status()` throws `HTTPError` for 4xx/5xx responses.

```python
# Line 27: Parse JSON
        raw_data = response.json()
```
- **Line 27:** Parses the response body into a Python list of dictionaries.

```python
# Line 29: Initialize output
        cleaned_portfolios = []
```
- **Line 29:** Empty accumulator list for processed entries.

```python
# Lines 31-34: Extract fields from each entry
        for item in raw_data:
            name = item.get("name", "Unknown")
            portfolio_url = item.get("url", "")
            role = item.get("tagline", "Developer")
```
- **Line 31:** Loops over each portfolio entry in the JSON array.
- **Line 32:** Extracts `name`, defaults to `"Unknown"` if missing.
- **Line 33:** Extracts `url`, named `portfolio_url` to avoid variable shadowing.
- **Line 34:** Extracts `tagline` as the role — this is the actual field the repo uses for job titles. Defaults to `"Developer"` if absent.

```python
# Lines 36-40: Build output entry
            cleaned_portfolios.append({
                "name": name,
                "role": role,
                "url": portfolio_url,
            })
```
- **Lines 36–40:** Creates a structured dictionary and appends to the output list.

```python
# Line 42: Return
        return cleaned_portfolios
```
- **Line 42:** Returns the full list of 1,806 parsed portfolios.

```python
# Lines 44-46: Error handling
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
```
- **Line 44:** Catches all `requests` exceptions (timeouts, connection errors, HTTP errors).
- **Line 45:** Logs the error to console.
- **Line 46:** Returns empty list so the API gracefully degrades with `count: 0`.

---
*Last Updated: 2026-07-02 (Day 2 — Replaced regex parsing with tagline field extraction)*
