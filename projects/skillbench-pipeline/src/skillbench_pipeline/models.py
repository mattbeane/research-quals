"""Pydantic models for request/response validation."""

from enum import Enum

from pydantic import BaseModel, Field


class SizeTier(str, Enum):
    enterprise = "enterprise"
    mid_market = "mid-market"
    startup = "startup"
    academic = "academic"


class Stage(str, Enum):
    lead = "lead"
    qualified = "qualified"
    proposal = "proposal"
    negotiation = "negotiation"
    won = "won"
    lost = "lost"


class DealType(str, Enum):
    assessment = "assessment"
    platform_arr = "platform_arr"
    research = "research"
    other = "other"


class ActivityType(str, Enum):
    email = "email"
    meeting = "meeting"
    call = "call"
    slack = "slack"
    note = "note"
    document = "document"
    other = "other"


class Direction(str, Enum):
    inbound = "inbound"
    outbound = "outbound"
    internal = "internal"


class RoleType(str, Enum):
    champion = "champion"
    decision_maker = "decision_maker"
    influencer = "influencer"
    user = "user"
    other = "other"


# ── Organizations ──────────────────────────────────────────────────────────

class OrgCreate(BaseModel):
    name: str
    domain: str | None = None
    industry: str | None = None
    size_tier: SizeTier | None = None
    notes: str | None = None
    drive_folder_path: str | None = None


class OrgUpdate(BaseModel):
    name: str | None = None
    domain: str | None = None
    industry: str | None = None
    size_tier: SizeTier | None = None
    notes: str | None = None
    drive_folder_path: str | None = None


class OrgResponse(BaseModel):
    id: int
    name: str
    domain: str | None = None
    industry: str | None = None
    size_tier: str | None = None
    notes: str | None = None
    drive_folder_path: str | None = None
    created_at: str
    updated_at: str
    deal_count: int = 0
    active_value_cents: int = 0


# ── Contacts ───────────────────────────────────────────────────────────────

class ContactCreate(BaseModel):
    org_id: int | None = None
    name: str
    email: str | None = None
    title: str | None = None
    role_type: RoleType | None = None
    phone: str | None = None
    notes: str | None = None


class ContactUpdate(BaseModel):
    org_id: int | None = None
    name: str | None = None
    email: str | None = None
    title: str | None = None
    role_type: RoleType | None = None
    phone: str | None = None
    notes: str | None = None


# ── Opportunities ──────────────────────────────────────────────────────────

class OppCreate(BaseModel):
    org_id: int
    title: str
    stage: Stage = Stage.lead
    deal_type: DealType | None = None
    value_cents: int = 0
    probability: int = Field(default=0, ge=0, le=100)
    expected_close_date: str | None = None
    contact_id: int | None = None
    notes: str | None = None


class OppUpdate(BaseModel):
    title: str | None = None
    deal_type: DealType | None = None
    value_cents: int | None = None
    probability: int | None = Field(default=None, ge=0, le=100)
    expected_close_date: str | None = None
    contact_id: int | None = None
    loss_reason: str | None = None
    notes: str | None = None


class StageUpdate(BaseModel):
    stage: Stage


# ── Activities ─────────────────────────────────────────────────────────────

class ActivityCreate(BaseModel):
    org_id: int | None = None
    opportunity_id: int | None = None
    contact_id: int | None = None
    activity_type: ActivityType
    direction: Direction | None = None
    subject: str | None = None
    summary: str | None = None
    source: str | None = None
    source_id: str | None = None
    source_url: str | None = None
    occurred_at: str | None = None


# ── Reminders ──────────────────────────────────────────────────────────────

class ReminderCreate(BaseModel):
    opportunity_id: int | None = None
    org_id: int | None = None
    contact_id: int | None = None
    reminder_text: str
    due_date: str
