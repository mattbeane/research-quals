# Pipeline Feed — Juho Setup

## What this does

Your Claude Code automatically scans your email and calendar each weekday morning, finds customer-related activity, and posts structured updates to `#bizdev` in Slack. Matt's pipeline tool reads those updates and ingests them into the shared pipeline database. Fully automatic on both sides.

## Setup (5 minutes)

### 1. Create a scheduled task in Claude Code

Open Claude Code and run:

```
/schedule
```

Create a task called `pipeline-feed` with this schedule: `27 9 * * 1-5` (weekday mornings at ~9:27am)

Use this prompt:

---

You are Juho's pipeline feed agent. Scan Gmail and Google Calendar for SkillBench customer activity from the last 24 hours, then post structured updates to #bizdev in Slack.

## What to scan

**Gmail**: Search for emails from/to these domains (last 24 hours):
microsoft.com, commbank.com.au, mckinsey.com, vanguard.com, hearst.com, sofi.org, walmart.com, amazon.com, verizon.com, gitlab.com, adidas.com, fidelity.com, nationwide.com, ghco.com, jcrew.com, spglobal.com, teamraderie.com

Also search: subject:(SOW OR proposal OR contract OR pilot OR assessment OR NDA OR skillbench)

**Google Calendar**: Check yesterday's and today's events for attendees from those domains.

## What to post

Post ONE message to #bizdev (channel_id: C0AQEDRMMQS) with this exact format:

```
PIPELINE UPDATE

ACTIVITY | Org: Microsoft | Type: email | Direction: outbound | Summary: Discussed pricing for Phase 2 | Date: 2026-04-02
ACTIVITY | Org: Vanguard | Type: meeting | Direction: inbound | Summary: MSA review call with Tracy | Date: 2026-04-02
```

If you discover a genuinely new opportunity (not already tracked), add:

```
NEW_DEAL | Org: NewCompany | Title: NewCompany Assessment | Value: 50000 | Type: assessment | Stage: lead | Notes: Brief context of how this came about
```

If you meet a new contact worth tracking:

```
CONTACT | Org: CompanyName | Name: Person Name | Email: person@company.com | Title: Their Title | Role: champion
```

## Rules
- Only log genuinely business-relevant emails. Skip newsletters, automated stuff.
- Keep summaries under 100 chars.
- If nothing relevant found, post: `PIPELINE UPDATE\n\nNo new customer activity today.`
- End every message with `<@U073L5HTMHC>` so Matt sees it.

---

### 2. First run

Click "Run now" on the task to approve tool permissions (Gmail, Slack, Calendar). After that it runs automatically.

### 3. That's it

Matt's pipeline reads #bizdev every morning at ~9:15am and ingests your updates into the shared pipeline database at `http://matts-macbook-pro:8100`.

## Format reference

Each line must start with one of these prefixes:
- `ACTIVITY | Org: ... | Type: email/meeting/call/slack/note | Direction: inbound/outbound/internal | Summary: ... | Date: YYYY-MM-DD`
- `NEW_DEAL | Org: ... | Title: ... | Value: dollars | Type: assessment/platform_arr/research/other | Stage: lead/qualified/proposal/negotiation | Notes: ...`
- `CONTACT | Org: ... | Name: ... | Email: ... | Title: ... | Role: champion/decision_maker/influencer/user`
- `REMINDER | Org: ... | Date: YYYY-MM-DD | Text: ...`
