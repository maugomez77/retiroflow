"""RetiroFlow AI features — Claude-powered retreat intelligence."""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        from anthropic import Anthropic
        _client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
    return _client


def _ask(system: str, prompt: str, max_tokens: int = 2048) -> str:
    client = _get_client()
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def match_participant_retreat(participant: dict, available_retreats: list[dict]) -> dict:
    """Match a participant to the best retreats based on their profile."""
    system = (
        "You are RetiroFlow AI, a wellness retreat recommendation engine for Oaxaca, Mexico. "
        "Given a participant profile and available retreats, recommend the top 3 best matches. "
        "Consider: experience level, dietary needs, medical conditions, budget, and interests. "
        "Respond in JSON: {\"recommendations\": [{\"retreat_id\": str, \"retreat_name\": str, "
        "\"match_score\": float (0-1), \"reason_en\": str, \"reason_es\": str}]}"
    )
    prompt = f"Participant:\n{json.dumps(participant, default=str)}\n\nAvailable Retreats:\n{json.dumps(available_retreats, default=str)}"
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"recommendations": [], "raw": raw}


def optimize_pricing(center: dict, season: str, occupancy_pct: float) -> dict:
    """Suggest optimal pricing for a center given season and occupancy."""
    system = (
        "You are RetiroFlow AI pricing optimizer for Oaxaca wellness retreats. "
        "Given a retreat center, current season, and occupancy rate, suggest optimal pricing. "
        "Consider: Oaxaca market rates ($80-500/night range), seasonal demand, competition, "
        "and the center's positioning. "
        "Respond in JSON: {\"suggested_price_min\": float, \"suggested_price_max\": float, "
        "\"multiplier\": float, \"strategy_en\": str, \"strategy_es\": str, \"confidence\": float}"
    )
    prompt = f"Center:\n{json.dumps(center, default=str)}\nSeason: {season}\nOccupancy: {occupancy_pct}%"
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def generate_retreat_description(retreat: dict, center: dict, facilitators: list[dict]) -> dict:
    """Generate bilingual marketing copy for a retreat."""
    system = (
        "You are RetiroFlow AI copywriter for Oaxaca wellness retreats. "
        "Generate compelling retreat descriptions in both English and Spanish. "
        "Capture the magic of Oaxaca: the coast, mountains, ancestral traditions, and healing arts. "
        "Respond in JSON: {\"description_en\": str (200-300 words), \"description_es\": str (200-300 words), "
        "\"tagline_en\": str, \"tagline_es\": str, \"highlights\": [str]}"
    )
    prompt = (
        f"Retreat:\n{json.dumps(retreat, default=str)}\n"
        f"Center:\n{json.dumps(center, default=str)}\n"
        f"Facilitators:\n{json.dumps(facilitators, default=str)}"
    )
    raw = _ask(system, prompt, max_tokens=3000)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def analyze_reviews(reviews: list[dict]) -> dict:
    """Analyze review sentiment and extract improvement suggestions."""
    system = (
        "You are RetiroFlow AI review analyst for Oaxaca wellness retreats. "
        "Analyze the reviews and provide: overall sentiment, key themes (positive and negative), "
        "and specific improvement suggestions. "
        "Respond in JSON: {\"overall_sentiment\": str, \"avg_rating\": float, "
        "\"positive_themes\": [str], \"negative_themes\": [str], "
        "\"improvements_en\": [str], \"improvements_es\": [str], "
        "\"summary_en\": str, \"summary_es\": str}"
    )
    prompt = f"Reviews:\n{json.dumps(reviews, default=str)}"
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def forecast_bookings(center: dict, season: str) -> dict:
    """Predict booking demand for a center in a given season."""
    system = (
        "You are RetiroFlow AI demand forecaster for Oaxaca wellness retreats. "
        "Based on the center profile, season, and Oaxaca tourism patterns, predict booking demand. "
        "Oaxaca peak: Nov-Feb (dry season, N.American winter). Shoulder: Mar-May. Low: Jun-Aug (rain). Fall: Sep-Oct. "
        "Respond in JSON: {\"predicted_occupancy_pct\": float, \"predicted_bookings_monthly\": int, "
        "\"demand_level\": str (low/medium/high/very_high), "
        "\"factors\": [str], \"recommendation_en\": str, \"recommendation_es\": str}"
    )
    prompt = f"Center:\n{json.dumps(center, default=str)}\nSeason: {season}"
    raw = _ask(system, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def plan_retreat_curriculum(retreat_type: str, duration_days: int, level: str) -> dict:
    """Generate an AI-powered retreat schedule/curriculum."""
    system = (
        "You are RetiroFlow AI retreat planner for Oaxaca, Mexico. "
        "Create a detailed day-by-day retreat curriculum. Include specific times, activities, meals, "
        "and optional excursions to Oaxacan cultural sites. Incorporate local traditions where appropriate "
        "(temazcal, cacao ceremony, Oaxacan cuisine, mezcal ceremony, visits to Monte Alban/Hierve el Agua). "
        "Respond in JSON: {\"title_en\": str, \"title_es\": str, \"overview_en\": str, \"overview_es\": str, "
        "\"daily_schedule\": [{\"day\": int, \"theme\": str, "
        "\"activities\": [{\"time\": str, \"activity\": str, \"description\": str}]}], "
        "\"materials_needed\": [str], \"facilitator_requirements\": [str]}"
    )
    prompt = f"Type: {retreat_type}\nDuration: {duration_days} days\nLevel: {level}"
    raw = _ask(system, prompt, max_tokens=4096)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}
