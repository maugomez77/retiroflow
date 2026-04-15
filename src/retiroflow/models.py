"""RetiroFlow data models."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --- Enums ---

class LocationType(str, Enum):
    oaxaca_city = "oaxaca_city"
    hierve_el_agua = "hierve_el_agua"
    mazunte = "mazunte"
    zipolite = "zipolite"
    huatulco = "huatulco"
    san_jose_del_pacifico = "san_jose_del_pacifico"
    monte_alban_area = "monte_alban_area"


class CenterType(str, Enum):
    yoga = "yoga"
    meditation = "meditation"
    healing = "healing"
    temazcal = "temazcal"
    mixed = "mixed"
    ayahuasca = "ayahuasca"
    wellness_spa = "wellness_spa"


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    paid = "paid"
    checked_in = "checked_in"
    completed = "completed"
    cancelled = "cancelled"
    refunded = "refunded"


class RetreatStatus(str, Enum):
    upcoming = "upcoming"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class AccommodationType(str, Enum):
    shared = "shared"
    private = "private"
    camping = "camping"
    luxury = "luxury"


class FacilitatorAvailability(str, Enum):
    available = "available"
    booked = "booked"
    unavailable = "unavailable"


class ServiceType(str, Enum):
    transportation = "transportation"
    catering = "catering"
    accommodation = "accommodation"
    excursion = "excursion"
    ceremony = "ceremony"
    photography = "photography"


class SeasonName(str, Enum):
    peak_winter = "peak_winter"
    shoulder_spring = "shoulder_spring"
    low_summer = "low_summer"
    peak_fall = "peak_fall"


class InsightType(str, Enum):
    booking_trend = "booking_trend"
    pricing = "pricing"
    demand = "demand"
    seasonal = "seasonal"
    facilitator_gap = "facilitator_gap"


class Specialty(str, Enum):
    yoga = "yoga"
    meditation = "meditation"
    breathwork = "breathwork"
    temazcal = "temazcal"
    herbalism = "herbalism"
    massage = "massage"
    sound_healing = "sound_healing"
    reiki = "reiki"


# --- Models ---

def _uid() -> str:
    return uuid.uuid4().hex[:12]


class RetreatCenter(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    location: LocationType
    center_type: CenterType
    capacity: int
    price_range_usd: dict = Field(default_factory=lambda: {"min": 0, "max": 0})
    amenities: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=lambda: ["es", "en"])
    certifications: list[str] = Field(default_factory=list)
    rating: float = 4.0
    photos: list[str] = Field(default_factory=list)
    owner: str = ""
    contact: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Retreat(BaseModel):
    id: str = Field(default_factory=_uid)
    center_id: str
    name: str
    description: str = ""
    center_type: CenterType
    start_date: date
    end_date: date
    duration_days: int = 7
    price_usd: float
    max_participants: int = 20
    current_participants: int = 0
    facilitator_ids: list[str] = Field(default_factory=list)
    status: RetreatStatus = RetreatStatus.upcoming
    meals_included: bool = True
    accommodation_type: AccommodationType = AccommodationType.shared


class Participant(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    email: str
    country: str = "US"
    dietary_restrictions: list[str] = Field(default_factory=list)
    medical_conditions: list[str] = Field(default_factory=list)
    experience_level: ExperienceLevel = ExperienceLevel.beginner
    retreat_ids: list[str] = Field(default_factory=list)
    total_spent_usd: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Facilitator(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    specialties: list[Specialty] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=lambda: ["es"])
    hourly_rate_usd: float = 50.0
    bio: str = ""
    rating: float = 4.5
    availability: FacilitatorAvailability = FacilitatorAvailability.available
    location: LocationType = LocationType.oaxaca_city


class Booking(BaseModel):
    id: str = Field(default_factory=_uid)
    retreat_id: str
    participant_id: str
    status: BookingStatus = BookingStatus.pending
    amount_usd: float = 0.0
    deposit_usd: float = 0.0
    payment_method: str = "card"
    booking_date: date = Field(default_factory=date.today)
    special_requests: str = ""
    dietary_notes: str = ""


class LocalService(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    service_type: ServiceType
    provider: str = ""
    contact: str = ""
    price_range_usd: dict = Field(default_factory=lambda: {"min": 0, "max": 0})
    description: str = ""
    rating: float = 4.0
    location: LocationType = LocationType.oaxaca_city


class Review(BaseModel):
    id: str = Field(default_factory=_uid)
    retreat_id: str
    participant_id: str
    rating: float = 4.0
    comment: str = ""
    aspects: dict = Field(default_factory=lambda: {
        "instruction": 4.0, "accommodation": 4.0,
        "food": 4.0, "location": 4.0, "value": 4.0,
    })
    review_date: str = Field(default_factory=lambda: __import__('datetime').date.today().isoformat())


class SeasonalPricing(BaseModel):
    id: str = Field(default_factory=_uid)
    center_id: str
    season: SeasonName
    multiplier: float = 1.0
    start_month: int
    end_month: int
    notes: str = ""


class WellnessInsight(BaseModel):
    id: str = Field(default_factory=_uid)
    insight_type: InsightType
    title: str
    description: str
    priority: str = "medium"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DashboardStats(BaseModel):
    total_centers: int = 0
    total_retreats_active: int = 0
    total_participants: int = 0
    monthly_revenue_usd: float = 0.0
    avg_occupancy_pct: float = 0.0
    top_retreat_types: list[dict] = Field(default_factory=list)
    upcoming_retreats: list[dict] = Field(default_factory=list)
