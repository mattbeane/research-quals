"""Reminder routes."""

from fastapi import APIRouter

from skillbench_pipeline.config import Settings
from skillbench_pipeline.db import complete_reminder, create_reminder, list_reminders
from skillbench_pipeline.models import ReminderCreate

router = APIRouter(tags=["reminders"])


def _db() -> str:
    return str(Settings().db_abs_path)


@router.get("/reminders")
async def api_list_reminders(overdue: bool = False, include_completed: bool = False):
    return await list_reminders(_db(), overdue_only=overdue, include_completed=include_completed)


@router.post("/reminders")
async def api_create_reminder(body: ReminderCreate):
    reminder_id = await create_reminder(_db(), **body.model_dump(exclude_none=True))
    return {"id": reminder_id}


@router.patch("/reminders/{reminder_id}/complete")
async def api_complete_reminder(reminder_id: int):
    await complete_reminder(_db(), reminder_id)
    return {"ok": True}
