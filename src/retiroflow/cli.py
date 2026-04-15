"""RetiroFlow CLI — wellness retreat management for Oaxaca."""

from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns

from . import store, ai
from .demo_data import seed_demo_data

app = typer.Typer(
    name="retiroflow",
    help="AI-powered wellness retreat management & booking for Oaxaca, Mexico",
    no_args_is_help=True,
)
console = Console()

LOCATION_EMOJI = {
    "mazunte": "🏖️", "zipolite": "🌊", "huatulco": "🏝️",
    "oaxaca_city": "🏛️", "hierve_el_agua": "⛰️",
    "san_jose_del_pacifico": "☁️", "monte_alban_area": "🏔️",
}

TYPE_EMOJI = {
    "yoga": "🧘", "meditation": "🧘‍♂️", "healing": "🌿",
    "temazcal": "🔥", "mixed": "✨", "ayahuasca": "🌱",
    "wellness_spa": "💆",
}

STATUS_COLOR = {
    "upcoming": "cyan", "active": "green", "completed": "dim",
    "cancelled": "red", "pending": "yellow", "confirmed": "blue",
    "paid": "green", "checked_in": "magenta", "refunded": "red",
}


# ─── Status ───

@app.command()
def status():
    """Show RetiroFlow system status and dashboard stats."""
    stats = store.compute_stats()
    console.print(Panel(
        f"[bold]Retreat Centers:[/] {stats['total_centers']}  |  "
        f"[bold]Active Retreats:[/] {stats['total_retreats_active']}  |  "
        f"[bold]Participants:[/] {stats['total_participants']}\n"
        f"[bold]Monthly Revenue:[/] ${stats['monthly_revenue_usd']:,.2f}  |  "
        f"[bold]Avg Occupancy:[/] {stats['avg_occupancy_pct']:.1f}%",
        title="[bold green]RetiroFlow Dashboard[/]",
        subtitle="Oaxaca Wellness Retreat Management",
        border_style="green",
    ))
    if stats["top_retreat_types"]:
        console.print("\n[bold]Top Retreat Types:[/]")
        for t in stats["top_retreat_types"]:
            emoji = TYPE_EMOJI.get(t["type"], "📋")
            console.print(f"  {emoji} {t['type']}: {t['count']} retreats")
    if stats["upcoming_retreats"]:
        console.print("\n[bold]Upcoming Retreats:[/]")
        for r in stats["upcoming_retreats"][:5]:
            console.print(f"  📅 {r['name']} — {r['start_date']}")


# ─── Demo ───

@app.command()
def demo():
    """Load demo data (12 centers, 20 retreats, 30 participants, etc.)."""
    data = seed_demo_data()
    console.print(Panel(
        f"[green]Demo data loaded![/]\n\n"
        f"  🏡 Retreat Centers: {len(data['centers'])}\n"
        f"  🧘 Retreats: {len(data['retreats'])}\n"
        f"  👤 Participants: {len(data['participants'])}\n"
        f"  🎓 Facilitators: {len(data['facilitators'])}\n"
        f"  📋 Bookings: {len(data['bookings'])}\n"
        f"  🚐 Local Services: {len(data['services'])}\n"
        f"  ⭐ Reviews: {len(data['reviews'])}\n"
        f"  💰 Seasonal Pricing: {len(data['pricing'])}\n"
        f"  💡 AI Insights: {len(data['insights'])}",
        title="[bold green]RetiroFlow Demo Data[/]",
        border_style="green",
    ))


# ─── Centers ───

@app.command()
def centers(
    location: Optional[str] = typer.Option(None, "--location", "-l", help="Filter by location"),
    type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by type"),
):
    """List retreat centers."""
    items = store.get_collection("centers")
    if location:
        items = [c for c in items if c.get("location") == location]
    if type:
        items = [c for c in items if c.get("type") == type]
    if not items:
        console.print("[yellow]No centers found.[/]")
        return
    table = Table(title=f"Retreat Centers ({len(items)})", border_style="green")
    table.add_column("Name", style="bold")
    table.add_column("Location")
    table.add_column("Type")
    table.add_column("Capacity", justify="right")
    table.add_column("Price (USD/night)", justify="right")
    table.add_column("Rating", justify="center")
    for c in items:
        loc = c.get("location", "")
        loc_display = f"{LOCATION_EMOJI.get(loc, '')} {loc.replace('_', ' ').title()}"
        tp = c.get("type", "")
        tp_display = f"{TYPE_EMOJI.get(tp, '')} {tp.replace('_', ' ').title()}"
        pr = c.get("price_range_usd", {})
        price = f"${pr.get('min', 0)}-${pr.get('max', 0)}"
        rating = f"{'⭐' * int(c.get('rating', 0))} {c.get('rating', 0)}"
        table.add_row(c["name"], loc_display, tp_display, str(c.get("capacity", 0)), price, rating)
    console.print(table)


# ─── Retreats ───

@app.command()
def retreats(
    status_filter: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by type"),
):
    """List retreats."""
    items = store.get_collection("retreats")
    if status_filter:
        items = [r for r in items if r.get("status") == status_filter]
    if type:
        items = [r for r in items if r.get("type") == type]
    if not items:
        console.print("[yellow]No retreats found.[/]")
        return
    table = Table(title=f"Retreats ({len(items)})", border_style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Type")
    table.add_column("Dates")
    table.add_column("Price", justify="right")
    table.add_column("Occupancy", justify="center")
    table.add_column("Status")
    for r in items:
        tp = TYPE_EMOJI.get(r.get("type", ""), "") + " " + r.get("type", "").replace("_", " ").title()
        dates = f"{r.get('start_date', '')} to {r.get('end_date', '')}"
        cur = r.get("current_participants", 0)
        mx = r.get("max_participants", 0)
        occ = f"{cur}/{mx} ({cur/mx*100:.0f}%)" if mx > 0 else "0/0"
        st = r.get("status", "")
        st_color = STATUS_COLOR.get(st, "white")
        table.add_row(r["name"], tp, dates, f"${r.get('price_usd', 0):,.0f}", occ, f"[{st_color}]{st}[/]")
    console.print(table)


# ─── Participants ───

@app.command()
def participants(
    country: Optional[str] = typer.Option(None, "--country", "-c", help="Filter by country"),
):
    """List participants."""
    items = store.get_collection("participants")
    if country:
        items = [p for p in items if p.get("country", "").upper() == country.upper()]
    if not items:
        console.print("[yellow]No participants found.[/]")
        return
    table = Table(title=f"Participants ({len(items)})", border_style="blue")
    table.add_column("Name", style="bold")
    table.add_column("Country")
    table.add_column("Level")
    table.add_column("Retreats", justify="right")
    table.add_column("Spent (USD)", justify="right")
    table.add_column("Dietary")
    for p in items:
        diet = ", ".join(p.get("dietary_restrictions", [])) or "-"
        table.add_row(
            p["name"], p.get("country", ""),
            p.get("experience_level", ""),
            str(len(p.get("retreat_ids", []))),
            f"${p.get('total_spent_usd', 0):,.0f}",
            diet,
        )
    console.print(table)


# ─── Facilitators ───

@app.command()
def facilitators(
    specialty: Optional[str] = typer.Option(None, "--specialty", "-s", help="Filter by specialty"),
):
    """List facilitators."""
    items = store.get_collection("facilitators")
    if specialty:
        items = [f for f in items if specialty in f.get("specialties", [])]
    if not items:
        console.print("[yellow]No facilitators found.[/]")
        return
    table = Table(title=f"Facilitators ({len(items)})", border_style="magenta")
    table.add_column("Name", style="bold")
    table.add_column("Specialties")
    table.add_column("Languages")
    table.add_column("Rate ($/hr)", justify="right")
    table.add_column("Rating", justify="center")
    table.add_column("Status")
    for f in items:
        specs = ", ".join(f.get("specialties", []))
        langs = ", ".join(f.get("languages", []))
        st = f.get("availability", "")
        st_color = {"available": "green", "booked": "yellow", "unavailable": "red"}.get(st, "white")
        table.add_row(f["name"], specs, langs, f"${f.get('hourly_rate_usd', 0):.0f}", f"⭐ {f.get('rating', 0)}", f"[{st_color}]{st}[/]")
    console.print(table)


# ─── Bookings ───

@app.command()
def bookings(
    status_filter: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
):
    """List bookings."""
    items = store.get_collection("bookings")
    if status_filter:
        items = [b for b in items if b.get("status") == status_filter]
    if not items:
        console.print("[yellow]No bookings found.[/]")
        return
    all_retreats = {r["id"]: r["name"] for r in store.get_collection("retreats")}
    all_participants = {p["id"]: p["name"] for p in store.get_collection("participants")}
    table = Table(title=f"Bookings ({len(items)})", border_style="yellow")
    table.add_column("ID", style="dim")
    table.add_column("Retreat")
    table.add_column("Participant")
    table.add_column("Amount", justify="right")
    table.add_column("Status")
    table.add_column("Date")
    for b in items:
        st = b.get("status", "")
        st_color = STATUS_COLOR.get(st, "white")
        table.add_row(
            b["id"],
            all_retreats.get(b.get("retreat_id", ""), b.get("retreat_id", ""))[:30],
            all_participants.get(b.get("participant_id", ""), b.get("participant_id", "")),
            f"${b.get('amount_usd', 0):,.0f}",
            f"[{st_color}]{st}[/]",
            str(b.get("booking_date", "")),
        )
    console.print(table)


# ─── Services ───

@app.command()
def services(
    type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by service type"),
):
    """List local services."""
    items = store.get_collection("services")
    if type:
        items = [s for s in items if s.get("type") == type]
    if not items:
        console.print("[yellow]No services found.[/]")
        return
    table = Table(title=f"Local Services ({len(items)})", border_style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Type")
    table.add_column("Provider")
    table.add_column("Price (USD)", justify="right")
    table.add_column("Location")
    table.add_column("Rating", justify="center")
    for s in items:
        pr = s.get("price_range_usd", {})
        price = f"${pr.get('min', 0)}-${pr.get('max', 0)}"
        loc = s.get("location", "").replace("_", " ").title()
        table.add_row(s["name"], s.get("type", ""), s.get("provider", ""), price, loc, f"⭐ {s.get('rating', 0)}")
    console.print(table)


# ─── Reviews ───

@app.command()
def reviews(
    retreat_id: Optional[str] = typer.Option(None, "--retreat", "-r", help="Filter by retreat"),
):
    """List reviews."""
    items = store.get_collection("reviews")
    if retreat_id:
        items = [r for r in items if r.get("retreat_id") == retreat_id]
    if not items:
        console.print("[yellow]No reviews found.[/]")
        return
    all_retreats = {r["id"]: r["name"] for r in store.get_collection("retreats")}
    all_participants = {p["id"]: p["name"] for p in store.get_collection("participants")}
    for r in items:
        retreat_name = all_retreats.get(r.get("retreat_id", ""), "Unknown")
        par_name = all_participants.get(r.get("participant_id", ""), "Unknown")
        stars = "⭐" * int(r.get("rating", 0))
        aspects = r.get("aspects", {})
        aspect_str = " | ".join(f"{k}: {v}" for k, v in aspects.items())
        console.print(Panel(
            f"[bold]{stars} {r.get('rating', 0)}/5[/]\n"
            f"[italic]{r.get('comment', '')}[/]\n\n"
            f"[dim]{aspect_str}[/]",
            title=f"{par_name} on {retreat_name}",
            subtitle=str(r.get("date", "")),
            border_style="yellow",
        ))


# ─── Pricing ───

@app.command()
def pricing(
    center_id: Optional[str] = typer.Option(None, "--center", "-c", help="Filter by center"),
):
    """Show seasonal pricing."""
    items = store.get_collection("pricing")
    if center_id:
        items = [p for p in items if p.get("center_id") == center_id]
    if not items:
        console.print("[yellow]No pricing data found.[/]")
        return
    all_centers = {c["id"]: c["name"] for c in store.get_collection("centers")}
    table = Table(title=f"Seasonal Pricing ({len(items)})", border_style="green")
    table.add_column("Center")
    table.add_column("Season")
    table.add_column("Months")
    table.add_column("Multiplier", justify="right")
    table.add_column("Notes")
    for p in items:
        center_name = all_centers.get(p.get("center_id", ""), p.get("center_id", ""))
        months = f"{p.get('start_month', '?')}-{p.get('end_month', '?')}"
        mult = p.get("multiplier", 1.0)
        color = "green" if mult > 1.0 else "red" if mult < 1.0 else "white"
        table.add_row(
            center_name[:25],
            p.get("season", "").replace("_", " ").title(),
            months,
            f"[{color}]{mult:.2f}x[/]",
            p.get("notes", "")[:50],
        )
    console.print(table)


# ─── Insights ───

@app.command()
def insights():
    """Show AI-generated wellness insights."""
    items = store.get_collection("insights")
    if not items:
        console.print("[yellow]No insights found.[/]")
        return
    for ins in items:
        priority = ins.get("priority", "medium")
        p_color = {"high": "red", "medium": "yellow", "low": "green"}.get(priority, "white")
        console.print(Panel(
            f"[bold]{ins.get('title', '')}[/]\n\n{ins.get('description', '')}",
            title=f"[{p_color}]{ins.get('insight_type', '').replace('_', ' ').upper()}[/] | Priority: [{p_color}]{priority.upper()}[/]",
            border_style=p_color,
        ))


# ─── AI Commands ───

@app.command()
def recommend(
    participant_id: str = typer.Argument(..., help="Participant ID to get recommendations for"),
):
    """AI: Match a participant to the best retreats."""
    participant = store.get_item("participants", participant_id)
    if not participant:
        console.print(f"[red]Participant {participant_id} not found.[/]")
        raise typer.Exit(1)
    available = [r for r in store.get_collection("retreats") if r.get("status") in ("upcoming", "active")]
    console.print(f"[cyan]Analyzing {participant['name']}'s profile against {len(available)} retreats...[/]\n")
    with console.status("[bold green]AI matching..."):
        result = ai.match_participant_retreat(participant, available)
    recs = result.get("recommendations", [])
    if not recs:
        console.print("[yellow]No recommendations generated.[/]")
        if "raw" in result:
            console.print(Panel(result["raw"], title="AI Response"))
        return
    for i, rec in enumerate(recs, 1):
        score_bar = "█" * int(rec.get("match_score", 0) * 10)
        console.print(Panel(
            f"[bold]Match Score:[/] {rec.get('match_score', 0):.0%} [{score_bar}]\n\n"
            f"[bold]EN:[/] {rec.get('reason_en', '')}\n"
            f"[bold]ES:[/] {rec.get('reason_es', '')}",
            title=f"#{i} {rec.get('retreat_name', '')}",
            border_style="green",
        ))


@app.command(name="optimize-pricing")
def optimize_pricing_cmd(
    center_id: str = typer.Argument(..., help="Center ID"),
    season: str = typer.Option("peak_winter", "--season", "-s", help="Season name"),
):
    """AI: Optimize pricing for a center and season."""
    center = store.get_item("centers", center_id)
    if not center:
        console.print(f"[red]Center {center_id} not found.[/]")
        raise typer.Exit(1)
    console.print(f"[cyan]Optimizing pricing for {center['name']} ({season})...[/]\n")
    retreats_list = [r for r in store.get_collection("retreats") if r.get("center_id") == center_id and r.get("status") in ("upcoming", "active")]
    total_cap = sum(r.get("max_participants", 0) for r in retreats_list) or 1
    total_cur = sum(r.get("current_participants", 0) for r in retreats_list)
    occ = total_cur / total_cap * 100
    with console.status("[bold green]AI optimizing..."):
        result = ai.optimize_pricing(center, season, occ)
    if "raw" in result:
        console.print(Panel(result["raw"], title="AI Response"))
        return
    console.print(Panel(
        f"[bold]Suggested Range:[/] ${result.get('suggested_price_min', 0):.0f} - ${result.get('suggested_price_max', 0):.0f}/night\n"
        f"[bold]Multiplier:[/] {result.get('multiplier', 1.0):.2f}x\n"
        f"[bold]Confidence:[/] {result.get('confidence', 0):.0%}\n\n"
        f"[bold]Strategy (EN):[/] {result.get('strategy_en', '')}\n"
        f"[bold]Strategy (ES):[/] {result.get('strategy_es', '')}",
        title=f"Pricing Optimization — {center['name']}",
        border_style="green",
    ))


@app.command(name="plan-retreat")
def plan_retreat_cmd(
    type: str = typer.Option("yoga", "--type", "-t", help="Retreat type"),
    duration: int = typer.Option(7, "--duration", "-d", help="Duration in days"),
    level: str = typer.Option("intermediate", "--level", "-l", help="Experience level"),
):
    """AI: Generate a retreat curriculum."""
    console.print(f"[cyan]Planning {duration}-day {type} retreat ({level} level)...[/]\n")
    with console.status("[bold green]AI planning curriculum..."):
        result = ai.plan_retreat_curriculum(type, duration, level)
    if "raw" in result:
        console.print(Panel(result["raw"], title="AI Response"))
        return
    console.print(Panel(
        f"[bold]{result.get('title_en', '')}[/]\n"
        f"[italic]{result.get('title_es', '')}[/]\n\n"
        f"{result.get('overview_en', '')}\n\n"
        f"[italic]{result.get('overview_es', '')}[/]",
        title="Retreat Curriculum",
        border_style="green",
    ))
    for day in result.get("daily_schedule", []):
        console.print(f"\n[bold cyan]Day {day.get('day', '?')}: {day.get('theme', '')}[/]")
        for act in day.get("activities", []):
            console.print(f"  {act.get('time', '')}  [bold]{act.get('activity', '')}[/]")
            if act.get("description"):
                console.print(f"         [dim]{act['description']}[/]")
    if result.get("materials_needed"):
        console.print("\n[bold]Materials Needed:[/]")
        for m in result["materials_needed"]:
            console.print(f"  - {m}")
    if result.get("facilitator_requirements"):
        console.print("\n[bold]Facilitator Requirements:[/]")
        for f in result["facilitator_requirements"]:
            console.print(f"  - {f}")


# ─── Serve ───

@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h"),
    port: int = typer.Option(8000, "--port", "-p"),
):
    """Start the RetiroFlow API server."""
    import uvicorn
    console.print(Panel(
        f"[bold green]RetiroFlow API starting[/]\n"
        f"  Host: {host}\n"
        f"  Port: {port}\n"
        f"  Docs: http://{host}:{port}/docs",
        title="RetiroFlow Server",
        border_style="green",
    ))
    uvicorn.run("retiroflow.api:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    app()
