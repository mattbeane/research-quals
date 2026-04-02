"""Seed database from Google Drive customer folders and known deals."""

from pathlib import Path

from skillbench_pipeline.db import create_org, create_opportunity, init_db

DRIVE_BASE = Path.home() / "Library/CloudStorage/GoogleDrive-matt@skillbench.com/Shared drives"

# Folder paths to scan for organizations
CUSTOMER_DIRS = [
    DRIVE_BASE / "SkillBench General" / "Customer",
    DRIVE_BASE / "SkillBench Founder" / "Customer",
    DRIVE_BASE / "SkillBench General" / "Biz Dev",
]

# Folders to skip (not actual orgs)
SKIP_NAMES = {"ARCHIVE", "Archive", "Expenses", "General"}

# Files to skip (not folders)
SKIP_EXTENSIONS = {".pdf", ".pptx", ".docx", ".xlsx", ".mov"}

# Domain mappings for known organizations
DOMAINS = {
    "Microsoft": "microsoft.com",
    "CommBank": "commbank.com.au",
    "McKinsey": "mckinsey.com",
    "OpenAI": "openai.com",
    "OpenAI - Research": "openai.com",
    "Vanguard": "vanguard.com",
    "BP": "bp.com",
    "Bain": "bain.com",
    "DTE Energy": "dteenergy.com",
    "Fannie Mae": "fanniemae.com",
    "Oliver Wyman": "oliverwyman.com",
    "Procore": "procore.com",
    "Starbucks": "starbucks.com",
    "UpWork": "upwork.com",
    "Walmart": "walmart.com",
    "Amazon": "amazon.com",
    "Andela": "andela.com",
    "Atlassian": "atlassian.com",
    "GitLabs": "gitlab.com",
    "Verizon": "verizon.com",
    "Asana": "asana.com",
}

# Size classifications
SIZES = {
    "Microsoft": "enterprise", "CommBank": "enterprise", "McKinsey": "enterprise",
    "OpenAI": "enterprise", "OpenAI - Research": "enterprise",
    "Vanguard": "enterprise", "BP": "enterprise", "Bain": "enterprise",
    "DTE Energy": "enterprise", "Fannie Mae": "enterprise",
    "Oliver Wyman": "enterprise", "Procore": "mid-market",
    "Starbucks": "enterprise", "UpWork": "enterprise", "Walmart": "enterprise",
    "Amazon": "enterprise", "Andela": "mid-market", "Atlassian": "enterprise",
    "GitLabs": "enterprise", "Verizon": "enterprise", "Asana": "mid-market",
}

# Known deals based on document inspection
SEED_DEALS = [
    {
        "org": "Microsoft",
        "title": "Microsoft Phase 1 - RoleBench Assessment",
        "stage": "won",
        "deal_type": "assessment",
        "value_cents": 5_000_000,  # $50K
        "probability": 100,
        "notes": "Multi-phase SOWs, Phase 1 complete with reports delivered",
    },
    {
        "org": "Microsoft",
        "title": "Microsoft Phase 2 - Platform Expansion",
        "stage": "negotiation",
        "deal_type": "platform_arr",
        "value_cents": 50_000_000,  # $500K ARR
        "probability": 40,
        "notes": "Round 2 SOW in discussion",
    },
    {
        "org": "CommBank",
        "title": "CommBank Pilot - Causal Study",
        "stage": "won",
        "deal_type": "assessment",
        "value_cents": 5_000_000,  # $50K
        "probability": 100,
        "notes": "Executed SOW, commercial tracking in progress",
    },
    {
        "org": "McKinsey",
        "title": "McKinsey Services Agreement",
        "stage": "won",
        "deal_type": "assessment",
        "value_cents": 5_000_000,  # $50K
        "probability": 100,
        "notes": "Executed services agreement",
    },
    {
        "org": "Vanguard",
        "title": "Vanguard Assessment",
        "stage": "qualified",
        "deal_type": "assessment",
        "value_cents": 5_000_000,  # $50K
        "probability": 30,
        "notes": "NDA and vendor intake forms executed",
    },
    {
        "org": "OpenAI",
        "title": "OpenAI Research Collaboration",
        "stage": "qualified",
        "deal_type": "research",
        "value_cents": 0,
        "probability": 50,
        "notes": "Research customer relationship",
    },
]


def _normalize_org_name(name: str) -> str:
    """Normalize org names across drives."""
    if name == "OpenAI - Research":
        return "OpenAI"
    return name


async def run_seed(db_path: str) -> None:
    """Scan Google Drive folders and seed organizations + known deals."""
    import typer

    await init_db(db_path)
    seen_orgs: set[str] = set()
    org_count = 0

    # Phase 1: Orgs from Google Drive
    for customer_dir in CUSTOMER_DIRS:
        if not customer_dir.exists():
            typer.echo(f"  Skipping (not found): {customer_dir}")
            continue

        for entry in sorted(customer_dir.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name in SKIP_NAMES:
                continue

            name = _normalize_org_name(entry.name)
            if name in seen_orgs:
                continue
            seen_orgs.add(name)

            org_id = await create_org(
                db_path,
                name=name,
                domain=DOMAINS.get(entry.name) or DOMAINS.get(name),
                size_tier=SIZES.get(entry.name) or SIZES.get(name),
                drive_folder_path=str(entry),
            )
            org_count += 1
            typer.echo(f"  Org: {name} (#{org_id})")

    typer.echo(f"\nSeeded {org_count} organizations.")

    # Phase 2: Known deals
    deal_count = 0
    from skillbench_pipeline.db import get_org_by_name
    for deal in SEED_DEALS:
        org_row = await get_org_by_name(db_path, deal["org"])
        if not org_row:
            typer.echo(f"  Skipping deal (org not found): {deal['title']}")
            continue

        opp_id = await create_opportunity(
            db_path,
            org_id=org_row["id"],
            title=deal["title"],
            stage=deal["stage"],
            deal_type=deal["deal_type"],
            value_cents=deal["value_cents"],
            probability=deal["probability"],
            notes=deal.get("notes"),
        )
        deal_count += 1
        typer.echo(f"  Deal: {deal['title']} (#{opp_id})")

    typer.echo(f"\nSeeded {deal_count} deals.")
    typer.echo("Done. Run 'pipeline status' to see your pipeline.\n")
