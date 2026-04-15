"""RetiroFlow real-time data — DuckDuckGo search + Open-Meteo weather."""

from __future__ import annotations

import httpx

try:
    from ddgs import DDGS
except ImportError:
    DDGS = None  # type: ignore


async def search_retreat_prices(query: str = "oaxaca wellness retreat prices 2026") -> list[dict]:
    """Search current retreat pricing from the web."""
    if DDGS is None:
        return [{"title": "DuckDuckGo not installed", "body": "pip install duckduckgo-search"}]
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        return [{"title": r.get("title", ""), "body": r.get("body", ""), "href": r.get("href", "")} for r in results]
    except Exception as e:
        return [{"title": "Search error", "body": str(e)}]


async def search_wellness_trends(query: str = "wellness tourism oaxaca mexico trends") -> list[dict]:
    """Search wellness tourism trends."""
    if DDGS is None:
        return []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        return [{"title": r.get("title", ""), "body": r.get("body", "")} for r in results]
    except Exception:
        return []


async def get_oaxaca_weather(location: str = "coast") -> dict:
    """Get 7-day weather forecast for Oaxaca regions via Open-Meteo."""
    coords = {
        "coast": (15.67, -96.49),       # Mazunte/Zipolite
        "city": (17.07, -96.72),         # Oaxaca city
        "mountains": (16.18, -96.50),    # San Jose del Pacifico
        "huatulco": (15.77, -96.13),     # Huatulco
    }
    lat, lon = coords.get(location, coords["coast"])
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode"
        f"&timezone=America/Mexico_City&forecast_days=7"
    )
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        daily = data.get("daily", {})
        days = []
        dates = daily.get("time", [])
        for i, d in enumerate(dates):
            days.append({
                "date": d,
                "temp_max_c": daily.get("temperature_2m_max", [0])[i],
                "temp_min_c": daily.get("temperature_2m_min", [0])[i],
                "precip_mm": daily.get("precipitation_sum", [0])[i],
                "code": daily.get("weathercode", [0])[i],
            })
        return {"location": location, "forecast": days}
    except Exception as e:
        return {"location": location, "error": str(e), "forecast": []}
