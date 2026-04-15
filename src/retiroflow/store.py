"""RetiroFlow JSON store — hybrid persistence layer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import (
    Booking, Facilitator, LocalService, Participant, Retreat, RetreatCenter,
    Review, SeasonalPricing, WellnessInsight,
)

STORE_DIR = Path.home() / ".retiroflow"
STORE_FILE = STORE_DIR / "store.json"

_MODEL_MAP: dict[str, type] = {
    "centers": RetreatCenter,
    "retreats": Retreat,
    "participants": Participant,
    "facilitators": Facilitator,
    "bookings": Booking,
    "services": LocalService,
    "reviews": Review,
    "pricing": SeasonalPricing,
    "insights": WellnessInsight,
}


def _ensure_dir() -> None:
    STORE_DIR.mkdir(parents=True, exist_ok=True)


def load_store() -> dict[str, list[dict]]:
    _ensure_dir()
    if STORE_FILE.exists():
        return json.loads(STORE_FILE.read_text())
    return {k: [] for k in _MODEL_MAP}


def save_store(data: dict[str, list[dict]]) -> None:
    _ensure_dir()
    STORE_FILE.write_text(json.dumps(data, indent=2, default=str))


def get_collection(name: str) -> list[dict]:
    return load_store().get(name, [])


def add_item(collection: str, item: dict) -> dict:
    store = load_store()
    store.setdefault(collection, []).append(item)
    save_store(store)
    return item


def update_item(collection: str, item_id: str, updates: dict) -> dict | None:
    store = load_store()
    for item in store.get(collection, []):
        if item.get("id") == item_id:
            item.update(updates)
            save_store(store)
            return item
    return None


def delete_item(collection: str, item_id: str) -> bool:
    store = load_store()
    items = store.get(collection, [])
    before = len(items)
    store[collection] = [i for i in items if i.get("id") != item_id]
    if len(store[collection]) < before:
        save_store(store)
        return True
    return False


def get_item(collection: str, item_id: str) -> dict | None:
    for item in get_collection(collection):
        if item.get("id") == item_id:
            return item
    return None


def count_collection(collection: str) -> int:
    return len(get_collection(collection))


def compute_stats() -> dict[str, Any]:
    store = load_store()
    centers = store.get("centers", [])
    retreats = store.get("retreats", [])
    participants = store.get("participants", [])
    bookings = store.get("bookings", [])

    active = [r for r in retreats if r.get("status") in ("upcoming", "active")]
    paid_bookings = [b for b in bookings if b.get("status") in ("paid", "confirmed", "checked_in", "completed")]
    monthly_rev = sum(b.get("amount_usd", 0) for b in paid_bookings)

    occ_values = []
    for r in active:
        mx = r.get("max_participants", 1)
        cur = r.get("current_participants", 0)
        if mx > 0:
            occ_values.append(cur / mx * 100)

    type_counts: dict[str, int] = {}
    for r in retreats:
        t = r.get("type", "mixed")
        type_counts[t] = type_counts.get(t, 0) + 1
    top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "total_centers": len(centers),
        "total_retreats_active": len(active),
        "total_participants": len(participants),
        "monthly_revenue_usd": round(monthly_rev, 2),
        "avg_occupancy_pct": round(sum(occ_values) / len(occ_values), 1) if occ_values else 0.0,
        "top_retreat_types": [{"type": t, "count": c} for t, c in top_types],
        "upcoming_retreats": [
            {"id": r["id"], "name": r["name"], "start_date": r.get("start_date", "")}
            for r in active[:10]
        ],
    }
