"""
DevFolio Backend - Data Fetcher
Downloads and parses the feed.json file from the emmabostian/developer-portfolios repository.
Extracts developer names, portfolio URLs, and tagline-based job roles.
"""

import requests

# The raw URL for the feed.json file in the repository's master branch
FEED_URL = "https://raw.githubusercontent.com/emmabostian/developer-portfolios/master/feed.json"


def get_portfolio_data():
    """
    Fetches feed.json from GitHub, parses each entry to extract:
      - name: developer name
      - role: the "tagline" field (e.g., "Software Engineer"), defaults to "Developer"
      - url: the portfolio URL

    Returns:
        list[dict]: A list of cleaned portfolio dictionaries.
    """
    try:
        response = requests.get(FEED_URL, timeout=15)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
        raw_data = response.json()

        cleaned_portfolios = []

        for item in raw_data:
            name = item.get("name", "Unknown")
            portfolio_url = item.get("url", "")
            role = item.get("tagline", "Developer")  # tagline holds the job title

            cleaned_portfolios.append({
                "name": name,
                "role": role,
                "url": portfolio_url,
            })

        return cleaned_portfolios

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
