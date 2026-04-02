"""Database operations. SQLite via aiosqlite."""

from datetime import datetime, timezone

import aiosqlite

SCHEMA = """
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    domain TEXT,
    industry TEXT,
    size_tier TEXT CHECK(size_tier IN ('enterprise', 'mid-market', 'startup', 'academic')),
    notes TEXT,
    drive_folder_path TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id INTEGER,
    name TEXT NOT NULL,
    email TEXT,
    title TEXT,
    role_type TEXT CHECK(role_type IN ('champion', 'decision_maker', 'influencer', 'user', 'other')),
    phone TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE INDEX IF NOT EXISTS idx_contacts_org ON contacts(org_id);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);

CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    stage TEXT NOT NULL DEFAULT 'lead'
        CHECK(stage IN ('lead', 'qualified', 'proposal', 'negotiation', 'won', 'lost')),
    deal_type TEXT CHECK(deal_type IN ('assessment', 'platform_arr', 'research', 'other')),
    value_cents INTEGER DEFAULT 0,
    currency TEXT DEFAULT 'USD',
    probability INTEGER DEFAULT 0 CHECK(probability >= 0 AND probability <= 100),
    expected_close_date TEXT,
    contact_id INTEGER,
    loss_reason TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    closed_at TEXT,
    FOREIGN KEY (org_id) REFERENCES organizations(id),
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);
CREATE INDEX IF NOT EXISTS idx_opps_stage ON opportunities(stage);
CREATE INDEX IF NOT EXISTS idx_opps_org ON opportunities(org_id);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER,
    org_id INTEGER,
    contact_id INTEGER,
    activity_type TEXT NOT NULL
        CHECK(activity_type IN ('email', 'meeting', 'call', 'slack', 'note', 'document', 'other')),
    direction TEXT CHECK(direction IN ('inbound', 'outbound', 'internal')),
    subject TEXT,
    summary TEXT,
    source TEXT,
    source_id TEXT,
    source_url TEXT,
    occurred_at TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id),
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);
CREATE INDEX IF NOT EXISTS idx_activities_opp ON activities(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_activities_org ON activities(org_id);
CREATE INDEX IF NOT EXISTS idx_activities_occurred ON activities(occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_activities_source_id ON activities(source_id);

CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER,
    org_id INTEGER,
    contact_id INTEGER,
    reminder_text TEXT NOT NULL,
    due_date TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    completed_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);
CREATE INDEX IF NOT EXISTS idx_reminders_due ON reminders(due_date) WHERE completed = 0;

CREATE TABLE IF NOT EXISTS stage_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL,
    from_stage TEXT,
    to_stage TEXT NOT NULL,
    changed_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
);

CREATE TABLE IF NOT EXISTS ingestion_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    ingested_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(source, source_id)
);
"""

_now = lambda: datetime.now(timezone.utc).isoformat()


async def init_db(db_path: str) -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.executescript(SCHEMA)
        await db.commit()


# ── Organizations ──────────────────────────────────────────────────────────

async def create_org(db_path: str, *, name: str, domain: str | None = None,
                     industry: str | None = None, size_tier: str | None = None,
                     notes: str | None = None, drive_folder_path: str | None = None) -> int:
    async with aiosqlite.connect(db_path) as db:
        cur = await db.execute(
            """INSERT INTO organizations (name, domain, industry, size_tier, notes, drive_folder_path)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(name) DO UPDATE SET
                   domain = COALESCE(excluded.domain, domain),
                   industry = COALESCE(excluded.industry, industry),
                   size_tier = COALESCE(excluded.size_tier, size_tier),
                   notes = COALESCE(excluded.notes, notes),
                   drive_folder_path = COALESCE(excluded.drive_folder_path, drive_folder_path),
                   updated_at = datetime('now')
               RETURNING id""",
            (name, domain, industry, size_tier, notes, drive_folder_path),
        )
        row = await cur.fetchone()
        await db.commit()
        return row[0]


async def list_orgs(db_path: str) -> list[dict]:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """SELECT o.*, COUNT(op.id) as deal_count,
                      SUM(CASE WHEN op.stage NOT IN ('won', 'lost') THEN op.value_cents ELSE 0 END) as active_value_cents
               FROM organizations o
               LEFT JOIN opportunities op ON op.org_id = o.id
               GROUP BY o.id ORDER BY o.name"""
        )
        return [dict(r) for r in await cur.fetchall()]


async def get_org(db_path: str, org_id: int) -> dict | None:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM organizations WHERE id = ?", (org_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def get_org_by_name(db_path: str, name: str) -> dict | None:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM organizations WHERE name = ?", (name,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def update_org(db_path: str, org_id: int, **fields) -> None:
    allowed = {"name", "domain", "industry", "size_tier", "notes", "drive_folder_path"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not updates:
        return
    updates["updated_at"] = _now()
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            f"UPDATE organizations SET {set_clause} WHERE id = ?",
            (*updates.values(), org_id),
        )
        await db.commit()


# ── Contacts ───────────────────────────────────────────────────────────────

async def create_contact(db_path: str, *, org_id: int | None = None, name: str,
                         email: str | None = None, title: str | None = None,
                         role_type: str | None = None, phone: str | None = None,
                         notes: str | None = None) -> int:
    async with aiosqlite.connect(db_path) as db:
        cur = await db.execute(
            """INSERT INTO contacts (org_id, name, email, title, role_type, phone, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id""",
            (org_id, name, email, title, role_type, phone, notes),
        )
        row = await cur.fetchone()
        await db.commit()
        return row[0]


async def list_contacts(db_path: str, org_id: int | None = None) -> list[dict]:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        if org_id:
            cur = await db.execute(
                """SELECT c.*, o.name as org_name FROM contacts c
                   LEFT JOIN organizations o ON o.id = c.org_id
                   WHERE c.org_id = ? ORDER BY c.name""",
                (org_id,),
            )
        else:
            cur = await db.execute(
                """SELECT c.*, o.name as org_name FROM contacts c
                   LEFT JOIN organizations o ON o.id = c.org_id
                   ORDER BY c.name"""
            )
        return [dict(r) for r in await cur.fetchall()]


async def update_contact(db_path: str, contact_id: int, **fields) -> None:
    allowed = {"org_id", "name", "email", "title", "role_type", "phone", "notes"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not updates:
        return
    updates["updated_at"] = _now()
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            f"UPDATE contacts SET {set_clause} WHERE id = ?",
            (*updates.values(), contact_id),
        )
        await db.commit()


# ── Opportunities ──────────────────────────────────────────────────────────

async def create_opportunity(db_path: str, *, org_id: int, title: str,
                             stage: str = "lead", deal_type: str | None = None,
                             value_cents: int = 0, probability: int = 0,
                             expected_close_date: str | None = None,
                             contact_id: int | None = None,
                             notes: str | None = None) -> int:
    async with aiosqlite.connect(db_path) as db:
        cur = await db.execute(
            """INSERT INTO opportunities
               (org_id, title, stage, deal_type, value_cents, probability,
                expected_close_date, contact_id, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id""",
            (org_id, title, stage, deal_type, value_cents, probability,
             expected_close_date, contact_id, notes),
        )
        row = await cur.fetchone()
        opp_id = row[0]
        # Record initial stage
        await db.execute(
            "INSERT INTO stage_history (opportunity_id, from_stage, to_stage) VALUES (?, NULL, ?)",
            (opp_id, stage),
        )
        await db.commit()
        return opp_id


async def list_opportunities(db_path: str, stage: str | None = None,
                             org_id: int | None = None) -> list[dict]:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        query = """SELECT op.*, o.name as org_name, c.name as contact_name,
                          (SELECT MAX(changed_at) FROM stage_history sh
                           WHERE sh.opportunity_id = op.id) as last_stage_change
                   FROM opportunities op
                   LEFT JOIN organizations o ON o.id = op.org_id
                   LEFT JOIN contacts c ON c.id = op.contact_id
                   WHERE 1=1"""
        params: list = []
        if stage:
            query += " AND op.stage = ?"
            params.append(stage)
        if org_id:
            query += " AND op.org_id = ?"
            params.append(org_id)
        query += " ORDER BY op.value_cents DESC"
        cur = await db.execute(query, params)
        return [dict(r) for r in await cur.fetchall()]


async def get_opportunity(db_path: str, opp_id: int) -> dict | None:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """SELECT op.*, o.name as org_name, c.name as contact_name
               FROM opportunities op
               LEFT JOIN organizations o ON o.id = op.org_id
               LEFT JOIN contacts c ON c.id = op.contact_id
               WHERE op.id = ?""",
            (opp_id,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None


async def update_opportunity(db_path: str, opp_id: int, **fields) -> None:
    allowed = {"title", "deal_type", "value_cents", "probability",
               "expected_close_date", "contact_id", "loss_reason", "notes"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not updates:
        return
    updates["updated_at"] = _now()
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            f"UPDATE opportunities SET {set_clause} WHERE id = ?",
            (*updates.values(), opp_id),
        )
        await db.commit()


async def delete_opportunity(db_path: str, opp_id: int) -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM stage_history WHERE opportunity_id = ?", (opp_id,))
        await db.execute("DELETE FROM activities WHERE opportunity_id = ?", (opp_id,))
        await db.execute("DELETE FROM reminders WHERE opportunity_id = ?", (opp_id,))
        await db.execute("DELETE FROM opportunities WHERE id = ?", (opp_id,))
        await db.commit()


async def move_opportunity_stage(db_path: str, opp_id: int, new_stage: str) -> None:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT stage FROM opportunities WHERE id = ?", (opp_id,))
        row = await cur.fetchone()
        if not row:
            raise ValueError(f"Opportunity {opp_id} not found")
        old_stage = row["stage"]
        if old_stage == new_stage:
            return

        now = _now()
        closed_at = now if new_stage in ("won", "lost") else None
        await db.execute(
            """UPDATE opportunities SET stage = ?, updated_at = ?, closed_at = COALESCE(?, closed_at)
               WHERE id = ?""",
            (new_stage, now, closed_at, opp_id),
        )
        await db.execute(
            "INSERT INTO stage_history (opportunity_id, from_stage, to_stage, changed_at) VALUES (?, ?, ?, ?)",
            (opp_id, old_stage, new_stage, now),
        )
        await db.commit()


# ── Activities ─────────────────────────────────────────────────────────────

async def create_activity(db_path: str, *, org_id: int | None = None,
                          opportunity_id: int | None = None,
                          contact_id: int | None = None,
                          activity_type: str, direction: str | None = None,
                          subject: str | None = None, summary: str | None = None,
                          source: str | None = None, source_id: str | None = None,
                          source_url: str | None = None,
                          occurred_at: str | None = None) -> int | None:
    if not occurred_at:
        occurred_at = _now()

    async with aiosqlite.connect(db_path) as db:
        # Dedup check
        if source and source_id:
            cur = await db.execute(
                "SELECT 1 FROM ingestion_log WHERE source = ? AND source_id = ?",
                (source, source_id),
            )
            if await cur.fetchone():
                return None  # Already ingested

        cur = await db.execute(
            """INSERT INTO activities
               (org_id, opportunity_id, contact_id, activity_type, direction,
                subject, summary, source, source_id, source_url, occurred_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id""",
            (org_id, opportunity_id, contact_id, activity_type, direction,
             subject, summary, source, source_id, source_url, occurred_at),
        )
        row = await cur.fetchone()
        activity_id = row[0]

        if source and source_id:
            await db.execute(
                "INSERT OR IGNORE INTO ingestion_log (source, source_id) VALUES (?, ?)",
                (source, source_id),
            )
        await db.commit()
        return activity_id


async def list_activities(db_path: str, org_id: int | None = None,
                          opportunity_id: int | None = None,
                          activity_type: str | None = None,
                          days: int | None = None,
                          limit: int = 50) -> list[dict]:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        query = """SELECT a.*, o.name as org_name, c.name as contact_name
                   FROM activities a
                   LEFT JOIN organizations o ON o.id = a.org_id
                   LEFT JOIN contacts c ON c.id = a.contact_id
                   WHERE 1=1"""
        params: list = []
        if org_id:
            query += " AND a.org_id = ?"
            params.append(org_id)
        if opportunity_id:
            query += " AND a.opportunity_id = ?"
            params.append(opportunity_id)
        if activity_type:
            query += " AND a.activity_type = ?"
            params.append(activity_type)
        if days:
            query += " AND a.occurred_at >= datetime('now', ?)"
            params.append(f"-{days} days")
        query += " ORDER BY a.occurred_at DESC LIMIT ?"
        params.append(limit)
        cur = await db.execute(query, params)
        return [dict(r) for r in await cur.fetchall()]


# ── Reminders ──────────────────────────────────────────────────────────────

async def create_reminder(db_path: str, *, opportunity_id: int | None = None,
                          org_id: int | None = None, contact_id: int | None = None,
                          reminder_text: str, due_date: str) -> int:
    async with aiosqlite.connect(db_path) as db:
        cur = await db.execute(
            """INSERT INTO reminders (opportunity_id, org_id, contact_id, reminder_text, due_date)
               VALUES (?, ?, ?, ?, ?) RETURNING id""",
            (opportunity_id, org_id, contact_id, reminder_text, due_date),
        )
        row = await cur.fetchone()
        await db.commit()
        return row[0]


async def list_reminders(db_path: str, overdue_only: bool = False,
                         include_completed: bool = False) -> list[dict]:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        query = """SELECT r.*, o.name as org_name, op.title as opp_title
                   FROM reminders r
                   LEFT JOIN organizations o ON o.id = r.org_id
                   LEFT JOIN opportunities op ON op.id = r.opportunity_id
                   WHERE 1=1"""
        params: list = []
        if not include_completed:
            query += " AND r.completed = 0"
        if overdue_only:
            query += " AND r.due_date < date('now') AND r.completed = 0"
        query += " ORDER BY r.due_date ASC"
        cur = await db.execute(query, params)
        return [dict(r) for r in await cur.fetchall()]


async def complete_reminder(db_path: str, reminder_id: int) -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "UPDATE reminders SET completed = 1, completed_at = ? WHERE id = ?",
            (_now(), reminder_id),
        )
        await db.commit()


# ── Dashboard aggregations ─────────────────────────────────────────────────

async def pipeline_summary(db_path: str) -> dict:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row

        # Stage counts and values
        cur = await db.execute(
            """SELECT stage, COUNT(*) as count, SUM(value_cents) as total_cents,
                      SUM(value_cents * probability / 100) as weighted_cents
               FROM opportunities
               GROUP BY stage"""
        )
        stages = {r["stage"]: dict(r) for r in await cur.fetchall()}

        # Active pipeline (excluding won/lost)
        cur = await db.execute(
            """SELECT COUNT(*) as active_deals,
                      SUM(value_cents) as active_value_cents,
                      SUM(value_cents * probability / 100) as weighted_value_cents
               FROM opportunities WHERE stage NOT IN ('won', 'lost')"""
        )
        active = dict(await cur.fetchone())

        # Overdue reminders
        cur = await db.execute(
            "SELECT COUNT(*) as count FROM reminders WHERE due_date < date('now') AND completed = 0"
        )
        overdue = (await cur.fetchone())[0]

        # Recent activity count (7 days)
        cur = await db.execute(
            "SELECT COUNT(*) as count FROM activities WHERE occurred_at >= datetime('now', '-7 days')"
        )
        recent_activities = (await cur.fetchone())[0]

        return {
            "stages": stages,
            "active_deals": active["active_deals"] or 0,
            "active_value_cents": active["active_value_cents"] or 0,
            "weighted_value_cents": active["weighted_value_cents"] or 0,
            "overdue_reminders": overdue,
            "recent_activities_7d": recent_activities,
        }


async def pipeline_velocity(db_path: str) -> list[dict]:
    """Average days spent in each stage for won deals."""
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """SELECT sh1.to_stage as stage,
                      AVG(julianday(COALESCE(sh2.changed_at, datetime('now'))) -
                          julianday(sh1.changed_at)) as avg_days
               FROM stage_history sh1
               LEFT JOIN stage_history sh2 ON sh2.opportunity_id = sh1.opportunity_id
                   AND sh2.from_stage = sh1.to_stage
               WHERE sh1.to_stage NOT IN ('won', 'lost')
               GROUP BY sh1.to_stage
               ORDER BY CASE sh1.to_stage
                   WHEN 'lead' THEN 1 WHEN 'qualified' THEN 2
                   WHEN 'proposal' THEN 3 WHEN 'negotiation' THEN 4 END"""
        )
        return [dict(r) for r in await cur.fetchall()]
