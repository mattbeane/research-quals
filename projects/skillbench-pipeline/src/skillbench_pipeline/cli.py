"""CLI entry point for SkillBench Pipeline."""

import asyncio

import typer

from skillbench_pipeline.config import Settings

app = typer.Typer(help="SkillBench Pipeline: Lightweight CRM for sales")


def _settings() -> Settings:
    return Settings()


def _db() -> str:
    return str(_settings().db_abs_path)


def _ensure_db() -> None:
    from skillbench_pipeline.db import init_db
    asyncio.run(init_db(_db()))


def _fmt_dollars(cents: int | None) -> str:
    if not cents:
        return "$0"
    return f"${cents / 100:,.0f}"


# ── Pipeline Status ────────────────────────────────────────────────────────

@app.command()
def status():
    """Show pipeline summary."""
    from skillbench_pipeline.db import pipeline_summary, list_reminders
    _ensure_db()
    summary = asyncio.run(pipeline_summary(_db()))
    reminders = asyncio.run(list_reminders(_db(), overdue_only=True))

    typer.echo("\n=== SkillBench Pipeline ===\n")

    stage_order = ["lead", "qualified", "proposal", "negotiation", "won", "lost"]
    for s in stage_order:
        info = summary["stages"].get(s, {})
        count = info.get("count", 0)
        total = _fmt_dollars(info.get("total_cents", 0))
        typer.echo(f"  {s:<14} {count:>3} deals  {total:>12}")

    typer.echo(f"\n  Active pipeline: {summary['active_deals']} deals, "
               f"{_fmt_dollars(summary['active_value_cents'])} total, "
               f"{_fmt_dollars(summary['weighted_value_cents'])} weighted")
    typer.echo(f"  Activities (7d): {summary['recent_activities_7d']}")
    typer.echo(f"  Overdue reminders: {summary['overdue_reminders']}")

    if reminders:
        typer.echo("\n  Overdue:")
        for r in reminders[:5]:
            typer.echo(f"    [{r['id']}] {r['due_date']} - {r['reminder_text']}")
    typer.echo()


# ── Deals ──────────────────────────────────────────────────────────────────

@app.command()
def deals(
    stage: str = typer.Option(None, help="Filter by stage"),
    org: str = typer.Option(None, help="Filter by organization name"),
):
    """List deals in the pipeline."""
    from skillbench_pipeline.db import list_opportunities, get_org_by_name
    _ensure_db()

    org_id = None
    if org:
        org_row = asyncio.run(get_org_by_name(_db(), org))
        if org_row:
            org_id = org_row["id"]
        else:
            typer.echo(f"Organization '{org}' not found.")
            raise typer.Exit(1)

    opps = asyncio.run(list_opportunities(_db(), stage=stage, org_id=org_id))
    if not opps:
        typer.echo("No deals found.")
        return

    typer.echo(f"\n{'ID':>4}  {'Stage':<14} {'Org':<20} {'Title':<30} {'Value':>12}")
    typer.echo("-" * 84)
    for o in opps:
        typer.echo(
            f"{o['id']:>4}  {o['stage']:<14} {(o['org_name'] or '')[:20]:<20} "
            f"{o['title'][:30]:<30} {_fmt_dollars(o['value_cents']):>12}"
        )
    typer.echo()


@app.command("deal-add")
def deal_add(
    org: str = typer.Option(..., help="Organization name"),
    title: str = typer.Option(..., help="Deal title"),
    value: int = typer.Option(0, help="Deal value in dollars"),
    stage: str = typer.Option("lead", help="Pipeline stage"),
    deal_type: str = typer.Option(None, help="Deal type: assessment, platform_arr, research, other"),
    probability: int = typer.Option(0, help="Win probability 0-100"),
    notes: str = typer.Option(None, help="Notes"),
):
    """Add a new deal."""
    from skillbench_pipeline.db import create_opportunity, create_org, get_org_by_name
    _ensure_db()

    org_row = asyncio.run(get_org_by_name(_db(), org))
    if not org_row:
        org_id = asyncio.run(create_org(_db(), name=org))
        typer.echo(f"Created org: {org}")
    else:
        org_id = org_row["id"]

    opp_id = asyncio.run(create_opportunity(
        _db(), org_id=org_id, title=title, stage=stage,
        deal_type=deal_type, value_cents=value * 100,
        probability=probability, notes=notes,
    ))
    typer.echo(f"Created deal #{opp_id}: {title} ({_fmt_dollars(value * 100)}) at {stage}")


@app.command("deal-move")
def deal_move(
    deal_id: int = typer.Argument(..., help="Deal ID"),
    stage: str = typer.Option(..., help="New stage"),
):
    """Move a deal to a new stage."""
    from skillbench_pipeline.db import move_opportunity_stage
    _ensure_db()
    asyncio.run(move_opportunity_stage(_db(), deal_id, stage))
    typer.echo(f"Deal #{deal_id} moved to {stage}")


# ── Organizations ──────────────────────────────────────────────────────────

@app.command()
def orgs():
    """List organizations."""
    from skillbench_pipeline.db import list_orgs
    _ensure_db()
    orgs_list = asyncio.run(list_orgs(_db()))
    if not orgs_list:
        typer.echo("No organizations found.")
        return

    typer.echo(f"\n{'ID':>4}  {'Name':<25} {'Size':<12} {'Deals':>5}  {'Active Value':>14}")
    typer.echo("-" * 66)
    for o in orgs_list:
        typer.echo(
            f"{o['id']:>4}  {o['name'][:25]:<25} {(o['size_tier'] or '-'):<12} "
            f"{o['deal_count']:>5}  {_fmt_dollars(o['active_value_cents']):>14}"
        )
    typer.echo()


@app.command("org-add")
def org_add(
    name: str = typer.Option(..., help="Organization name"),
    domain: str = typer.Option(None, help="Domain (e.g., microsoft.com)"),
    size: str = typer.Option(None, help="Size tier: enterprise, mid-market, startup, academic"),
    industry: str = typer.Option(None, help="Industry"),
    notes: str = typer.Option(None, help="Notes"),
):
    """Add an organization."""
    from skillbench_pipeline.db import create_org
    _ensure_db()
    org_id = asyncio.run(create_org(_db(), name=name, domain=domain,
                                    size_tier=size, industry=industry, notes=notes))
    typer.echo(f"Created org #{org_id}: {name}")


# ── Contacts ───────────────────────────────────────────────────────────────

@app.command()
def contacts(
    org: str = typer.Option(None, help="Filter by organization name"),
):
    """List contacts."""
    from skillbench_pipeline.db import list_contacts, get_org_by_name
    _ensure_db()

    org_id = None
    if org:
        org_row = asyncio.run(get_org_by_name(_db(), org))
        if org_row:
            org_id = org_row["id"]

    contacts_list = asyncio.run(list_contacts(_db(), org_id=org_id))
    if not contacts_list:
        typer.echo("No contacts found.")
        return

    typer.echo(f"\n{'ID':>4}  {'Name':<25} {'Org':<20} {'Role':<15} {'Email':<30}")
    typer.echo("-" * 98)
    for c in contacts_list:
        typer.echo(
            f"{c['id']:>4}  {c['name'][:25]:<25} {(c['org_name'] or '-')[:20]:<20} "
            f"{(c['role_type'] or '-'):<15} {(c['email'] or '-'):<30}"
        )
    typer.echo()


@app.command("contact-add")
def contact_add(
    org: str = typer.Option(..., help="Organization name"),
    name: str = typer.Option(..., help="Contact name"),
    email: str = typer.Option(None, help="Email"),
    title: str = typer.Option(None, help="Job title"),
    role: str = typer.Option(None, help="Role type: champion, decision_maker, influencer, user, other"),
):
    """Add a contact."""
    from skillbench_pipeline.db import create_contact, get_org_by_name, create_org
    _ensure_db()

    org_row = asyncio.run(get_org_by_name(_db(), org))
    if not org_row:
        org_id = asyncio.run(create_org(_db(), name=org))
    else:
        org_id = org_row["id"]

    contact_id = asyncio.run(create_contact(
        _db(), org_id=org_id, name=name, email=email,
        title=title, role_type=role,
    ))
    typer.echo(f"Created contact #{contact_id}: {name} at {org}")


# ── Activities ─────────────────────────────────────────────────────────────

@app.command()
def log(
    org: str = typer.Option(..., help="Organization name"),
    type: str = typer.Option(..., help="Type: email, meeting, call, slack, note, document, other"),
    summary: str = typer.Option(..., help="Activity summary"),
    direction: str = typer.Option(None, help="Direction: inbound, outbound, internal"),
    source: str = typer.Option(None, help="Source system (gmail, slack, gcal, etc.)"),
    source_id: str = typer.Option(None, help="Source ID for dedup"),
    occurred_at: str = typer.Option(None, help="When it occurred (ISO date)"),
):
    """Log an activity."""
    from skillbench_pipeline.db import create_activity, get_org_by_name
    _ensure_db()

    org_row = asyncio.run(get_org_by_name(_db(), org))
    if not org_row:
        typer.echo(f"Organization '{org}' not found. Use org-add first.")
        raise typer.Exit(1)

    activity_id = asyncio.run(create_activity(
        _db(), org_id=org_row["id"], activity_type=type,
        summary=summary, direction=direction,
        source=source, source_id=source_id, occurred_at=occurred_at,
    ))
    if activity_id:
        typer.echo(f"Logged activity #{activity_id}")
    else:
        typer.echo("Activity already logged (duplicate).")


# ── Reminders ──────────────────────────────────────────────────────────────

@app.command()
def reminders(
    overdue: bool = typer.Option(False, help="Show only overdue"),
):
    """List reminders."""
    from skillbench_pipeline.db import list_reminders
    _ensure_db()

    items = asyncio.run(list_reminders(_db(), overdue_only=overdue))
    if not items:
        typer.echo("No reminders." if not overdue else "No overdue reminders.")
        return

    typer.echo(f"\n{'ID':>4}  {'Due Date':<12} {'Org/Deal':<25} {'Reminder':<40}")
    typer.echo("-" * 85)
    for r in items:
        label = r.get("opp_title") or r.get("org_name") or "-"
        typer.echo(f"{r['id']:>4}  {r['due_date']:<12} {label[:25]:<25} {r['reminder_text'][:40]}")
    typer.echo()


@app.command()
def remind(
    deal: int = typer.Option(None, help="Deal ID to attach reminder to"),
    org: str = typer.Option(None, help="Organization name"),
    date: str = typer.Option(..., help="Due date (YYYY-MM-DD)"),
    text: str = typer.Option(..., help="Reminder text"),
):
    """Create a reminder."""
    from skillbench_pipeline.db import create_reminder, get_org_by_name
    _ensure_db()

    org_id = None
    if org:
        org_row = asyncio.run(get_org_by_name(_db(), org))
        if org_row:
            org_id = org_row["id"]

    reminder_id = asyncio.run(create_reminder(
        _db(), opportunity_id=deal, org_id=org_id,
        reminder_text=text, due_date=date,
    ))
    typer.echo(f"Created reminder #{reminder_id}: {text} (due {date})")


# ── Deal context (for automated assessment) ────────────────────────────────

@app.command("deal-context")
def deal_context(
    deal_id: int = typer.Argument(..., help="Deal ID"),
):
    """Dump all context for a deal as JSON (for AI assessment)."""
    import json
    from skillbench_pipeline.db import get_opportunity, list_activities, list_contacts, list_reminders
    _ensure_db()

    opp = asyncio.run(get_opportunity(_db(), deal_id))
    if not opp:
        typer.echo(f"Deal #{deal_id} not found.")
        raise typer.Exit(1)

    contacts = asyncio.run(list_contacts(_db(), org_id=opp["org_id"]))
    activities = asyncio.run(list_activities(_db(), org_id=opp["org_id"], limit=30))
    reminders_list = asyncio.run(list_reminders(_db()))
    deal_reminders = [r for r in reminders_list if r.get("opportunity_id") == deal_id]

    context = {
        "deal": opp,
        "contacts": contacts,
        "recent_activities": activities,
        "reminders": deal_reminders,
    }
    typer.echo(json.dumps(context, indent=2, default=str))


@app.command("deal-update-notes")
def deal_update_notes(
    deal_id: int = typer.Argument(..., help="Deal ID"),
    notes: str = typer.Option(..., help="New notes content"),
    probability: int = typer.Option(None, help="Updated probability 0-100"),
    value: int = typer.Option(None, help="Updated value in dollars"),
):
    """Update deal notes (and optionally probability/value) from assessment."""
    from skillbench_pipeline.db import update_opportunity
    _ensure_db()

    fields = {"notes": notes}
    if probability is not None:
        fields["probability"] = probability
    if value is not None:
        fields["value_cents"] = value * 100
    asyncio.run(update_opportunity(_db(), deal_id, **fields))
    typer.echo(f"Updated deal #{deal_id}")


# ── Server ─────────────────────────────────────────────────────────────────

@app.command()
def serve(
    port: int = typer.Option(None, help="Port (default from config)"),
    host: str = typer.Option(None, help="Host (default from config)"),
):
    """Start the web dashboard server."""
    import uvicorn
    _ensure_db()
    settings = _settings()
    uvicorn.run(
        "skillbench_pipeline.server:app",
        host=host or settings.host,
        port=port or settings.port,
        reload=True,
    )


# ── Seed ───────────────────────────────────────────────────────────────────

@app.command()
def seed():
    """Seed database from Google Drive customer folders."""
    from skillbench_pipeline.seed import run_seed
    _ensure_db()
    asyncio.run(run_seed(_db()))


if __name__ == "__main__":
    app()
