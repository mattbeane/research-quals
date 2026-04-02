"""Activity routes."""

from fastapi import APIRouter

from skillbench_pipeline.config import Settings
from skillbench_pipeline.db import create_activity, list_activities
from skillbench_pipeline.models import ActivityCreate

router = APIRouter(tags=["activities"])


def _db() -> str:
    return str(Settings().db_abs_path)


@router.get("/activities")
async def api_list_activities(
    org_id: int | None = None,
    opportunity_id: int | None = None,
    activity_type: str | None = None,
    days: int | None = None,
    limit: int = 50,
):
    return await list_activities(
        _db(), org_id=org_id, opportunity_id=opportunity_id,
        activity_type=activity_type, days=days, limit=limit,
    )


@router.post("/activities")
async def api_create_activity(body: ActivityCreate):
    activity_id = await create_activity(_db(), **body.model_dump(exclude_none=True))
    if activity_id is None:
        return {"id": None, "duplicate": True}
    return {"id": activity_id}
