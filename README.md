# DevFolio

A high-performance web aggregator that transforms the [emmabostian/developer-portfolios](https://github.com/emmabostian/developer-portfolios) GitHub repository into a visual, interactive gallery with hover-to-scroll previews.

## Tech Stack

- **Backend:** Python 3 + FastAPI + Playwright + Motor (async MongoDB)
- **Frontend:** HTML5, CSS3 (Grid), Vanilla JavaScript
- **Database:** MongoDB Atlas (GridFS for image storage)
- **Data Source:** `feed.json` from developer-portfolios repo

## Project Structure

```
devfolio/
├── venv/                        # Python virtual environment
├── backend/
│   ├── main.py                  # FastAPI server (API + static file serving)
│   ├── fetch_data.py            # feed.json fetcher, parser & exclusion filter
│   ├── excluded_names.py        # Set of 149 excluded portfolio names
│   ├── screenshot_service.py    # Playwright screenshot automation + MongoDB upload
│   └── mongo_client.py          # Motor async MongoDB GridFS client
├── frontend/
│   ├── index.html               # Grid container with filter bar & progress tracker
│   ├── styles.css               # Neo-Brutalist layout, themes & hover animations
│   └── app.js                   # Data fetching, role normalization & card rendering
├── requirements.txt             # Python dependencies
└── Info_folder/                 # Documentation for each source file
```

## Features

- **1,157 Developer Portfolios** curated from 1,806 entries (149 excluded, 500 pruned)
- **Hover-to-Scroll Previews** — 3-part incremental screenshots stitched vertically
- **Curated Role Filtering** — 25 clean role categories (AI/ML, Full Stack, Frontend, etc.)
- **Real-time Scraper Progress Bar** — live updates as screenshots are captured
- **Dark/Light Theme Toggle** — Manila Paper (light) and Dark Espresso (dark) themes
- **MongoDB Atlas GridFS** — persistent cloud storage for all screenshot images
- **Dynamic Card Updates** — placeholder cards swap to real screenshots without page reload

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
playwright install chromium
```

## Running

```bash
# Start the API server
uvicorn backend.main:app --reload --port 8000

# Start the screenshot scraper (separate terminal)
python backend/screenshot_service.py
```

## Environment Variables

Create a `.env` file (see `.env.example`):

```
MONGO_URI=mongodb+srv://...
MONGO_DB_NAME=devfolio
```
