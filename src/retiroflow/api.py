"""RetiroFlow FastAPI application."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from . import ai, realtime, store
from .models import (
    Booking, BookingStatus, CenterType, Facilitator, LocalService,
    Participant, Retreat, RetreatCenter, Review, SeasonalPricing, WellnessInsight,
)


async def _load_demo_if_empty():
    try:
        if not store.get_collection("centers"):
            from . import demo_data
            demo_data.seed_demo_data()
    except Exception as e:
        import traceback
        traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(_load_demo_if_empty())
    yield


app = FastAPI(
    title="RetiroFlow API",
    description="Wellness retreat management & booking for Oaxaca, Mexico",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health ---

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "retiroflow"}


# --- Dashboard ---

@app.get("/api/v1/stats")
def get_stats():
    return store.compute_stats()


# --- Centers ---

@app.get("/api/v1/centers")
def list_centers(location: str | None = None, type: str | None = None):
    items = store.get_collection("centers")
    if location:
        items = [c for c in items if c.get("location") == location]
    if type:
        items = [c for c in items if c.get("type") == type]
    return {"centers": items, "total": len(items)}


@app.get("/api/v1/centers/{center_id}")
def get_center(center_id: str):
    item = store.get_item("centers", center_id)
    if not item:
        raise HTTPException(404, "Center not found")
    return item


@app.post("/api/v1/centers")
def create_center(data: RetreatCenter):
    return store.add_item("centers", data.model_dump())


@app.put("/api/v1/centers/{center_id}")
def update_center(center_id: str, updates: dict):
    item = store.update_item("centers", center_id, updates)
    if not item:
        raise HTTPException(404, "Center not found")
    return item


@app.delete("/api/v1/centers/{center_id}")
def delete_center(center_id: str):
    if not store.delete_item("centers", center_id):
        raise HTTPException(404, "Center not found")
    return {"deleted": True}


# --- Retreats ---

@app.get("/api/v1/retreats")
def list_retreats(status: str | None = None, center_id: str | None = None, type: str | None = None):
    items = store.get_collection("retreats")
    if status:
        items = [r for r in items if r.get("status") == status]
    if center_id:
        items = [r for r in items if r.get("center_id") == center_id]
    if type:
        items = [r for r in items if r.get("type") == type]
    return {"retreats": items, "total": len(items)}


@app.get("/api/v1/retreats/{retreat_id}")
def get_retreat(retreat_id: str):
    item = store.get_item("retreats", retreat_id)
    if not item:
        raise HTTPException(404, "Retreat not found")
    return item


@app.post("/api/v1/retreats")
def create_retreat(data: Retreat):
    return store.add_item("retreats", data.model_dump())


@app.put("/api/v1/retreats/{retreat_id}")
def update_retreat(retreat_id: str, updates: dict):
    item = store.update_item("retreats", retreat_id, updates)
    if not item:
        raise HTTPException(404, "Retreat not found")
    return item


@app.delete("/api/v1/retreats/{retreat_id}")
def delete_retreat(retreat_id: str):
    if not store.delete_item("retreats", retreat_id):
        raise HTTPException(404, "Retreat not found")
    return {"deleted": True}


# --- Participants ---

@app.get("/api/v1/participants")
def list_participants(country: str | None = None, level: str | None = None):
    items = store.get_collection("participants")
    if country:
        items = [p for p in items if p.get("country") == country]
    if level:
        items = [p for p in items if p.get("experience_level") == level]
    return {"participants": items, "total": len(items)}


@app.get("/api/v1/participants/{pid}")
def get_participant(pid: str):
    item = store.get_item("participants", pid)
    if not item:
        raise HTTPException(404, "Participant not found")
    return item


@app.post("/api/v1/participants")
def create_participant(data: Participant):
    return store.add_item("participants", data.model_dump())


@app.put("/api/v1/participants/{pid}")
def update_participant(pid: str, updates: dict):
    item = store.update_item("participants", pid, updates)
    if not item:
        raise HTTPException(404, "Participant not found")
    return item


# --- Facilitators ---

@app.get("/api/v1/facilitators")
def list_facilitators(specialty: str | None = None, available: bool | None = None):
    items = store.get_collection("facilitators")
    if specialty:
        items = [f for f in items if specialty in f.get("specialties", [])]
    if available is not None:
        target = "available" if available else "booked"
        items = [f for f in items if f.get("availability") == target]
    return {"facilitators": items, "total": len(items)}


@app.get("/api/v1/facilitators/{fid}")
def get_facilitator(fid: str):
    item = store.get_item("facilitators", fid)
    if not item:
        raise HTTPException(404, "Facilitator not found")
    return item


@app.post("/api/v1/facilitators")
def create_facilitator(data: Facilitator):
    return store.add_item("facilitators", data.model_dump())


# --- Bookings ---

@app.get("/api/v1/bookings")
def list_bookings(status: str | None = None, retreat_id: str | None = None):
    items = store.get_collection("bookings")
    if status:
        items = [b for b in items if b.get("status") == status]
    if retreat_id:
        items = [b for b in items if b.get("retreat_id") == retreat_id]
    return {"bookings": items, "total": len(items)}


@app.get("/api/v1/bookings/{bid}")
def get_booking(bid: str):
    item = store.get_item("bookings", bid)
    if not item:
        raise HTTPException(404, "Booking not found")
    return item


@app.post("/api/v1/bookings")
def create_booking(data: Booking):
    d = data.model_dump()
    # Update retreat participant count
    retreat = store.get_item("retreats", d["retreat_id"])
    if retreat:
        current = retreat.get("current_participants", 0)
        mx = retreat.get("max_participants", 999)
        if current >= mx:
            raise HTTPException(400, "Retreat is full")
        store.update_item("retreats", d["retreat_id"], {"current_participants": current + 1})
    return store.add_item("bookings", d)


@app.put("/api/v1/bookings/{bid}")
def update_booking(bid: str, updates: dict):
    item = store.update_item("bookings", bid, updates)
    if not item:
        raise HTTPException(404, "Booking not found")
    return item


# --- Local Services ---

@app.get("/api/v1/services")
def list_services(type: str | None = None, location: str | None = None):
    items = store.get_collection("services")
    if type:
        items = [s for s in items if s.get("type") == type]
    if location:
        items = [s for s in items if s.get("location") == location]
    return {"services": items, "total": len(items)}


@app.post("/api/v1/services")
def create_service(data: LocalService):
    return store.add_item("services", data.model_dump())


# --- Reviews ---

@app.get("/api/v1/reviews")
def list_reviews(retreat_id: str | None = None):
    items = store.get_collection("reviews")
    if retreat_id:
        items = [r for r in items if r.get("retreat_id") == retreat_id]
    return {"reviews": items, "total": len(items)}


@app.post("/api/v1/reviews")
def create_review(data: Review):
    return store.add_item("reviews", data.model_dump())


# --- Pricing ---

@app.get("/api/v1/pricing")
def list_pricing(center_id: str | None = None):
    items = store.get_collection("pricing")
    if center_id:
        items = [p for p in items if p.get("center_id") == center_id]
    return {"pricing": items, "total": len(items)}


# --- Insights ---

@app.get("/api/v1/insights")
def list_insights():
    items = store.get_collection("insights")
    return {"insights": items, "total": len(items)}


# --- AI Endpoints ---

@app.post("/api/v1/ai/recommend")
def ai_recommend(participant_id: str = Query(...)):
    participant = store.get_item("participants", participant_id)
    if not participant:
        raise HTTPException(404, "Participant not found")
    retreats = [r for r in store.get_collection("retreats") if r.get("status") in ("upcoming", "active")]
    return ai.match_participant_retreat(participant, retreats)


@app.post("/api/v1/ai/optimize-pricing")
def ai_optimize_pricing(center_id: str = Query(...), season: str = Query("peak_winter")):
    center = store.get_item("centers", center_id)
    if not center:
        raise HTTPException(404, "Center not found")
    retreats = [r for r in store.get_collection("retreats") if r.get("center_id") == center_id and r.get("status") in ("upcoming", "active")]
    total_cap = sum(r.get("max_participants", 0) for r in retreats) or 1
    total_cur = sum(r.get("current_participants", 0) for r in retreats)
    occ = total_cur / total_cap * 100
    return ai.optimize_pricing(center, season, occ)


@app.post("/api/v1/ai/generate-description")
def ai_generate_description(retreat_id: str = Query(...)):
    retreat = store.get_item("retreats", retreat_id)
    if not retreat:
        raise HTTPException(404, "Retreat not found")
    center = store.get_item("centers", retreat.get("center_id", "")) or {}
    fac_ids = retreat.get("facilitator_ids", [])
    facilitators = [f for f in store.get_collection("facilitators") if f.get("id") in fac_ids]
    return ai.generate_retreat_description(retreat, center, facilitators)


@app.post("/api/v1/ai/analyze-reviews")
def ai_analyze_reviews(retreat_id: str = Query(...)):
    reviews = [r for r in store.get_collection("reviews") if r.get("retreat_id") == retreat_id]
    if not reviews:
        raise HTTPException(404, "No reviews found for this retreat")
    return ai.analyze_reviews(reviews)


@app.post("/api/v1/ai/forecast")
def ai_forecast(center_id: str = Query(...), season: str = Query("peak_winter")):
    center = store.get_item("centers", center_id)
    if not center:
        raise HTTPException(404, "Center not found")
    return ai.forecast_bookings(center, season)


@app.post("/api/v1/ai/plan-retreat")
def ai_plan_retreat(type: str = Query("yoga"), duration: int = Query(7), level: str = Query("intermediate")):
    return ai.plan_retreat_curriculum(type, duration, level)


# --- Real-Time Data ---

@app.get("/api/v1/weather")
async def get_weather(location: str = Query("coast")):
    return await realtime.get_oaxaca_weather(location)


@app.get("/api/v1/market-research")
async def market_research(query: str = Query("oaxaca wellness retreat prices 2026")):
    return {"results": await realtime.search_retreat_prices(query)}


@app.get("/api/v1/trends")
async def wellness_trends(query: str = Query("wellness tourism oaxaca mexico trends")):
    return {"results": await realtime.search_wellness_trends(query)}
